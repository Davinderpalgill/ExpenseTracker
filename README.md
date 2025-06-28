# 💸 Telegram Expense Tracker Bot

A cost-effective, privacy-focused Telegram bot to track your daily expenses.  
Send messages like `Groceries 450 cash` or `Rent 8000 online` directly to your bot, and it stores, categorizes, and summarizes your spending.

No third-party services required — runs 100% locally using Python, SQLite, and Telegram Bot API.

---

## ✨ Features

- 📩 Log expenses by sending simple messages
- 🧠 Intelligent parser extracts category, amount, type (cash/online), and receiver
- 📊 Get daily, weekly, and monthly summaries via bot commands
- 💰 View totals per category with breakdowns
- 🗃 Local SQLite storage — portable and efficient
- 🛠 Designed for easy deployment (Replit, Render, Railway, etc.)

## Commands
- /summary	Full summary (today + week + month)
- /summary_today	Shows today's expenses
- /summary_week	Shows current week's expenses
- /summary_month	Shows current month's expenses
