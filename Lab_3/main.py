from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os
import re


app = Flask(__name__)
app.secret_key = os.urandom(24)  # Важливо для забезпечення безпеки сесій

# Переконаємось, що база даних існує
DB_PATH = "database.sqlite"

# Перевірка валідності email за допомогою регулярного виразу
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

# Перевірка пароля (наприклад, мінімум 6 символів)
def is_valid_password(password):
    return len(password) >= 6


class OrderBuilder:
    def __init__(self, user):
        self.order = {'name': user, 'bike_type': None, 'date': None}

    def set_bike_type(self, bike_type):
        self.order['bike_type'] = bike_type
        return self

    def set_date(self, date):
        self.order['date'] = date
        return self

    def build(self):
        # Повертає побудоване замовлення
        return self.order


class Facade:
    @staticmethod
    def create_order(user, bike_type, date):
        # Використовуємо Builder для створення замовлення
        builder = OrderBuilder(user)
        order = builder.set_bike_type(bike_type).set_date(date).build()

        # Зберігаємо замовлення в базі даних
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("INSERT INTO orders (name, bike_type, date) VALUES (?, ?, ?)",
                    (order['name'], order['bike_type'], order['date']))
        conn.commit()
        conn.close()


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Створення таблиці користувачів
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)

    # Створення таблиці замовлень
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            bike_type TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Викликаємо ініціалізацію бази при запуску
init_db()


# Вихід з системи
@app.route('/logout')
def logout():
    session.pop('user', None)  # Видаляє користувача із сесії
    return redirect(url_for('index'))




# Головна сторінка
@app.route('/')
def index():
    return render_template('index.html')


# Сторінка реєстрації
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Перевірка валідності email
        if not is_valid_email(email):
            return "Невірний формат email!"

        # Перевірка пароля
        if not is_valid_password(password):
            return "Пароль повинен містити принаймні 6 символів!"

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        try:
            cur.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                        (name, email, password))
            conn.commit()

            # Зберігаємо користувача в сесії
            session['user'] = name  # Зберігаємо ім'я користувача в сесії

        except sqlite3.IntegrityError:
            return "Користувач або email вже існує!"

        conn.close()
        return redirect(url_for('index'))

    return render_template('register.html')


# Сторінка входу
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        # Перевірка на порожні поля
        if not name or not password:
            return "Ім'я користувача і пароль не можуть бути порожніми!"

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE name = ? AND password = ?", (name, password))
        user = cur.fetchone()
        conn.close()

        if user:
            session['user'] = name  # Зберігаємо користувача в сесії
            return redirect(url_for('index'))
        else:
            return "Неправильне ім'я користувача або пароль!"

    return render_template('login.html')

# Сторінка замовлення велосипеда
@app.route('/order', methods=['GET', 'POST'])
def order():
    if 'user' not in session:  # Перевірка, чи є користувач в сесії
        return redirect(url_for('register'))  # Якщо ні — перенаправити на сторінку реєстрації

    if request.method == 'POST':
        name = session['user']  # Використовуємо ім'я користувача з сесії
        bike_type = request.form['bike_type']
        date = request.form['date']

        # Використовуємо фасад для створення замовлення
        Facade.create_order(name, bike_type, date)

        return redirect(url_for('orders'))

    return render_template('order.html')




# Перегляд всіх замовлень
@app.route('/orders')
def orders():
    if 'user' not in session:  # Перевірка на авторизацію
        return redirect(url_for('register'))  # Якщо ні — перенаправити на сторінку реєстрації

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders")
    orders_list = cur.fetchall()
    conn.close()

    return render_template('orders.html', orders=orders_list)

@app.context_processor
def inject_user():
    return dict(session=session)  # Додає session у всі шаблони


if __name__ == '__main__':
    app.run(debug=True)
