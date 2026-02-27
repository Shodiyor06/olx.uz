import os

import requests
from dotenv import load_dotenv
from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

BACKEND_URL = "http://127.0.0.1:8000/api/v1/telegram/bot-login/"



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    button = KeyboardButton("📱 Send Contact", request_contact=True)

    reply_markup = ReplyKeyboardMarkup(
        [[button]], resize_keyboard=True, one_time_keyboard=True
    )

    await update.message.reply_text(
        "Welcome!\n\nPlease share your phone number to login:",
        reply_markup=reply_markup,
    )



async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact

    data = {
        "telegram_id": contact.user_id,
        "phone_number": contact.phone_number,
        "first_name": update.message.from_user.first_name,
    }

    try:
        response = requests.post(BACKEND_URL, json=data)
        result = response.json()

        code = result.get("code")

        await update.message.reply_text(
            f"🔐 Your login code:\n\n"
            f"{code}\n\n"
            "Enter this code on the website to login."
        )

    except Exception:
        await update.message.reply_text("Server error. Try again later.")



def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.CONTACT, contact_handler))

    print("Bot started...")

    app.run_polling()


if __name__ == "__main__":
    main()