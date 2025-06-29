import sqlite3
import pandas as pd
from datetime import datetime, timedelta

DB_PATH = "data/expenses.db"

def fetch_data(username=None):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM expenses", conn, parse_dates=["date"])
    conn.close()
    
    if username:
        df = df[df["username"] == username]
    
    df["date"] = pd.to_datetime(df["date"])
    return df

def category_summary_text(username, filter_func, label=""):
    df = fetch_data(username)
    df_filtered = df[filter_func(df)]

    if df_filtered.empty:
        return f"📊 *{label} Summary:*\nNo data for this period."

    # Separate credit and debit
    debit_df = df_filtered[df_filtered["transaction_type"] == "debit"]
    credit_df = df_filtered[df_filtered["transaction_type"] == "credit"]

    # Group debit categories
    category_totals = debit_df.groupby("category")["amount"].sum().sort_values(ascending=False)

    spent = debit_df["amount"].sum()
    credited = credit_df["amount"].sum()
    balance = credited - spent

    summary = f"📊 *{label} Summary:*\n"

    if not category_totals.empty:
        summary += "\n".join([f"{cat}: ₹{amt:.2f}" for cat, amt in category_totals.items()])
    else:
        summary += "No debit transactions."

    summary += f"\n\n💰 *Available Balance:* ₹{balance:.2f}"
    summary += f"\n🟢 *Credited:* ₹{credited:.2f} | 🔴 *Spent:* ₹{spent:.2f}"

    return summary


# === Filters === #

def is_today(df):
    today = datetime.today().date()
    return df['date'].dt.date == today

def is_yesterday(df):
    yesterday = datetime.today().date() - timedelta(days=1)
    return df['date'].dt.date == yesterday

def is_week(df):
    today = datetime.today()
    week_start = today - timedelta(days=today.weekday())  # Monday
    return (df['date'] >= week_start) & (df['date'] <= today)

def is_month(df):
    today = datetime.today()
    return (df['date'].dt.month == today.month) & (df['date'].dt.year == today.year)

def is_year(df):
    return df['date'].dt.year == datetime.today().year
