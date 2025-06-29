import sqlite3
from datetime import datetime

def parse_expense(text: str, username: str):
    tokens = text.strip().split()

    if len(tokens) < 2:
        print("❌ Invalid message format")
        return

    try:
        # Extract core fields
        category = tokens[0].capitalize()
        amount = float(tokens[1])
        transaction_type = 'debit'  # default type
        payment_mode = 'cash'       # default payment mode
        receiver = None

        # Detect credit transactions
        if 'credited' in text.lower() or category.lower() in ['credited', 'income', 'salary']:
            transaction_type = 'credit'
            if category.lower() == 'credited':
                category = 'Income'

        # Extract optional info: mode & receiver
        for token in tokens[2:]:
            token_lower = token.lower()
            if token_lower in ['cash', 'online']:
                payment_mode = token_lower
            elif token_lower != 'credited':
                receiver = token

        now = datetime.now()
        date = now.date().isoformat()
        time = now.strftime('%H:%M:%S')

        # Insert into DB
        conn = sqlite3.connect('data/expenses.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO expenses (username, date, time, category, amount, payment_mode, receiver, transaction_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (username, date, time, category, amount, payment_mode, receiver, transaction_type))

        conn.commit()
        conn.close()

        print(f"✅ {transaction_type.upper()} entry added for {username}: {category} - ₹{amount}")

    except Exception as e:
        print(f"❌ Error: {e}")
