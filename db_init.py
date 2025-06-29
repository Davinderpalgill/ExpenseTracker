# db_init.py
import sqlite3

conn = sqlite3.connect("data/expenses.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    date TIMESTAMP NOT NULL,
    time TEXT NOT NULL,
    category TEXT NOT NULL,
    amount REAL NOT NULL,
    payment_mode TEXT,
    receiver TEXT,
    transaction_type TEXT
)
""")

conn.commit()
conn.close()
print("✅ Database initialized.")
