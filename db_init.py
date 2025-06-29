# db_init.py

def initialize_db():
    import sqlite3
    import os
    os.makedirs('data', exist_ok=True)
    conn = sqlite3.connect('data/expenses.db')
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        date TEXT,
        time TEXT,
        category TEXT,
        amount REAL,
        payment_mode TEXT,
        receiver TEXT,
        transaction_type TEXT
    )
    """)
    conn.commit()
    conn.close()
    print("✅ Database initialized.")

if __name__ == "__main__":
    initialize_db()
