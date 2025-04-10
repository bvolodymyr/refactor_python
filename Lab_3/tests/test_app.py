import unittest
import sqlite3
import os
from main import is_valid_email, is_valid_password, Facade, OrderBuilder, init_db

TEST_DB = "test_database.sqlite"

class TestApp(unittest.TestCase):

    def setUp(self):
        # Створюємо тестову базу
        self.conn = sqlite3.connect(TEST_DB)
        self.cur = self.conn.cursor()

        self.cur.execute("DROP TABLE IF EXISTS users")
        self.cur.execute("DROP TABLE IF EXISTS orders")

        self.cur.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        """)

        self.cur.execute("""
            CREATE TABLE orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                bike_type TEXT NOT NULL,
                date TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def tearDown(self):
        self.conn.close()
        os.remove(TEST_DB)

    # --- Тестування окремих функцій ---

    def test_valid_email(self):
        self.assertTrue(is_valid_email("test@example.com"))
        self.assertFalse(is_valid_email("invalid-email"))

    def test_valid_password(self):
        self.assertTrue(is_valid_password("123456"))
        self.assertFalse(is_valid_password("123"))

    # --- Тестування OrderBuilder ---

    def test_order_builder(self):
        builder = OrderBuilder("Alice")
        order = builder.set_bike_type("Електро").set_date("2025-05-01").build()
        self.assertEqual(order['name'], "Alice")
        self.assertEqual(order['bike_type'], "Електро")
        self.assertEqual(order['date'], "2025-05-01")

    # --- Тестування Facade ---

    def test_create_order(self):
        Facade.create_order = self.facade_create_order_test_version  # заміна методa для тесту
        Facade.create_order("Bob", "Звичайний", "2025-06-15")

        self.cur.execute("SELECT * FROM orders WHERE name = ?", ("Bob",))
        result = self.cur.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[1], "Bob")
        self.assertEqual(result[2], "Звичайний")
        self.assertEqual(result[3], "2025-06-15")

    def facade_create_order_test_version(self, user, bike_type, date):
        builder = OrderBuilder(user)
        order = builder.set_bike_type(bike_type).set_date(date).build()
        self.cur.execute("INSERT INTO orders (name, bike_type, date) VALUES (?, ?, ?)",
                         (order['name'], order['bike_type'], order['date']))
        self.conn.commit()

    # --- Взаємодія між користувачем та замовленням ---

    def test_user_registration_and_order(self):
        self.cur.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                         ("Charlie", "charlie@example.com", "pass123"))
        self.conn.commit()

        self.cur.execute("SELECT * FROM users WHERE name = ?", ("Charlie",))
        user = self.cur.fetchone()
        self.assertIsNotNone(user)

        # Замовлення
        self.facade_create_order_test_version("Charlie", "Електро", "2025-07-10")
        self.cur.execute("SELECT * FROM orders WHERE name = ?", ("Charlie",))
        order = self.cur.fetchone()
        self.assertIsNotNone(order)
        self.assertEqual(order[2], "Електро")

    # --- Крайні випадки ---

    def test_empty_email(self):
        self.assertFalse(is_valid_email(""))

    def test_short_password(self):
        self.assertFalse(is_valid_password("a"))

    def test_duplicate_user(self):
        self.cur.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                         ("Daisy", "daisy@example.com", "pass123"))
        self.conn.commit()
        with self.assertRaises(sqlite3.IntegrityError):
            self.cur.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                             ("Daisy", "daisy@example.com", "pass123"))
            self.conn.commit()


if __name__ == '__main__':
    unittest.main()
