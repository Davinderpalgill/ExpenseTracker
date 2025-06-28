import sqlite3
import pandas as pd
from datetime import datetime, timedelta

DB_PATH = "data/expenses.db"

def fetch_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM expenses", conn, parse_dates=["date"])
    conn.close()
    return df

def category_summary_text(filter_func, label=""):
    df = fetch_data()
    df['date'] = pd.to_datetime(df['date'])
    df_filtered = df[filter_func(df)]

    if df_filtered.empty:
        return f"No data for {label}."

    result = df_filtered.groupby("category")["amount"].sum().sort_values(ascending=False)
    total = result.sum()

    summary = f"\n📊 *{label} Summary*:\n"
    summary += "\n".join([f"{cat}: ₹{amt:.2f}" for cat, amt in result.items()])
    summary += f"\n💰 *Total*: ₹{total:.2f}"

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
