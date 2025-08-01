import os
from dotenv import load_dotenv
import requests
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes,
)

load_dotenv()
API_URL = os.getenv("API_URL")
TOKEN = os.getenv("BOT_TOKEN")
# In-memory user storage for demo
user_data = {}

# States for conversation
NICKNAME, PICK = range(2)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Enter nickname to search:")
    return NICKNAME


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chosen = user_data.get(user_id)
    if not chosen:
        await update.message.reply_text("You have not picked anything yet. Use /start.")
        return
    resp = requests.get(f"{API_URL}/stats", params={"url": chosen})
    data = resp.json()["results"]
    # TODO: add formating
    # now returns just general stats for ground realistic
    await update.message.reply_text(f"Raw stats JSON:\n{data[1]}")


async def search_nickname(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    nickname = update.message.text.strip()
    resp = requests.get(f"{API_URL}/search", params={"q": nickname})
    data = resp.json()["results"]  # assuming it's {"nick1": "url1", ...}

    if not data:
        await update.message.reply_text("No results. Try another nickname:")
        return NICKNAME

    nicks = list(data.keys())
    context.user_data["nick_url_map"] = data  # save mapping for later use

    reply_markup = ReplyKeyboardMarkup([[n] for n in data], one_time_keyboard=True)
    await update.message.reply_text("Pick one:", reply_markup=reply_markup)
    return PICK


async def pick_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    picked_nick = update.message.text.strip()
    nick_url_map = context.user_data.get("nick_url_map", {})
    url = nick_url_map.get(picked_nick)

    if not url:
        await update.message.reply_text("Invalid choice, pick one from the list.")
        return PICK

    user_id = update.effective_user.id
    user_data[user_id] = url  # Store url only!
    await update.message.reply_text(
        f"Saved {picked_nick}! Use /stats to get your stats."
    )
    return ConversationHandler.END


def main():
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NICKNAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, search_nickname)
            ],
            PICK: [MessageHandler(filters.TEXT & ~filters.COMMAND, pick_choice)],
        },
        fallbacks=[CommandHandler("start", start)],
    )
    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("stats", stats))

    app.run_polling()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
