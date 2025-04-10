import sqlite3

import cursor

db = "database.sqlite"


conn = sqlite3.connect(db)
cursor = conn.cursor()

cursor.execute("SELECT * FROM orders")
rows = cursor.fetchall()

# Виведення вмісту таблиці
for row in rows:
    print(row)

# Закриття з'єднання
cursor.close()
conn.close()

