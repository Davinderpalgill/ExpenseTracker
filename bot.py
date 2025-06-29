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

# Bot token
BOT_TOKEN = "8139719801:AAEULb0_KYRYaZ-EEJXJ96Hqqdog6GzIQ7Q"

# Handle normal text messages (expenses)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text
    print(f"📩 Message from {user.username or user.first_name}: {text}")
    username = user.username or user.first_name
    parse_expense(text, username)

# /summary command (all summaries)
async def send_summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username or update.message.from_user.first_name
    today = category_summary_text(username, is_today, "Today")
    week = category_summary_text(username, is_week, "This Week")
    month = category_summary_text(username, is_month, "This Month")

    reply = f"📅 *Expense Summary for {username}*\n\n{today}\n\n{week}\n\n{month}"
    await update.message.reply_text(reply, parse_mode="Markdown")

# /summary_today
async def summary_today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username or update.message.from_user.first_name
    text = category_summary_text(username, is_today, "Today")
    await update.message.reply_text(text, parse_mode="Markdown")

# /summary_week
async def summary_week(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username or update.message.from_user.first_name
    text = category_summary_text(username, is_week, "This Week")
    await update.message.reply_text(text, parse_mode="Markdown")

# /summary_month
async def summary_month(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username or update.message.from_user.first_name
    text = category_summary_text(username, is_month, "This Month")
    await update.message.reply_text(text, parse_mode="Markdown")

# Bot application setup
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(CommandHandler("summary", send_summary))
app.add_handler(CommandHandler("summary_today", summary_today))
app.add_handler(CommandHandler("summary_week", summary_week))
app.add_handler(CommandHandler("summary_month", summary_month))

print("🤖 Bot is running... Press Ctrl+C to stop.")
app.run_polling()
