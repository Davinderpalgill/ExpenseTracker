import os
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters
)
from ingest.parser import parse_expense
from reports.summary import category_summary_text, is_today, is_week, is_month
from db_init import initialize_db

# Bot token
BOT_TOKEN = "8139719801:AAEULb0_KYRYaZ-EEJXJ96Hqqdog6GzIQ7Q"

# Initialize DB once
initialize_db()

# --- Handlers ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text
    print(f"📩 Message from {user.username or user.first_name}: {text}")
    username = user.username or user.first_name
    parse_expense(text, username)

async def send_summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username or update.message.from_user.first_name
    today = category_summary_text(username, is_today, "Today")
    week = category_summary_text(username, is_week, "This Week")
    month = category_summary_text(username, is_month, "This Month")
    reply = f"📅 *Expense Summary for {username}*\n\n{today}\n\n{week}\n\n{month}"
    await update.message.reply_text(reply, parse_mode="Markdown")

async def summary_today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username or update.message.from_user.first_name
    text = category_summary_text(username, is_today, "Today")
    await update.message.reply_text(text, parse_mode="Markdown")

async def summary_week(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username or update.message.from_user.first_name
    text = category_summary_text(username, is_week, "This Week")
    await update.message.reply_text(text, parse_mode="Markdown")

async def summary_month(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username or update.message.from_user.first_name
    text = category_summary_text(username, is_month, "This Month")
    await update.message.reply_text(text, parse_mode="Markdown")

# --- App Setup ---
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # 🔧 Fix for webhook conflict error
    await app.bot.delete_webhook(drop_pending_updates=True)

    # Register handlers
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CommandHandler("summary", send_summary))
    app.add_handler(CommandHandler("summary_today", summary_today))
    app.add_handler(CommandHandler("summary_week", summary_week))
    app.add_handler(CommandHandler("summary_month", summary_month))

    print("🤖 Bot is running... Press Ctrl+C to stop.")
    await app.run_polling()

# Run
if __name__ == "__main__":
    asyncio.run(main())
