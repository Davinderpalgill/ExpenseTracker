import sqlite3

conn = sqlite3.connect("data/expenses.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    date TEXT,
    time TEXT,
    category TEXT,
    amount REAL,
    payment_type TEXT,
    receiver TEXT,
    notes TEXT
)
""")

conn.commit()
conn.close()
print("✅ Database initialized.")
