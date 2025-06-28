import sqlite3
from datetime import datetime

def parse_expense(message: str, username: str):
    tokens = message.strip().split()
    
    if len(tokens) < 3:
        print("❌ Invalid message format. Use: <Category> <Amount> <Type> [Receiver] [Notes]")
        return

    category = tokens[0].capitalize()
    try:
        amount = float(tokens[1])
    except ValueError:
        print("❌ Amount must be a number.")
        return

    payment_type = tokens[2].lower()  # cash/online
    receiver = tokens[3] if len(tokens) >= 4 else ""
    notes = " ".join(tokens[4:]) if len(tokens) >= 5 else ""

    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M")

    conn = sqlite3.connect("data/expenses.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO expenses (username, date, time, category, amount, payment_type, receiver, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (username, date, time, category, amount, payment_type, receiver, notes))
    conn.commit()
    conn.close()

    print(f"✅ Stored: {category} ₹{amount} via {payment_type} to {receiver} — {notes}")
