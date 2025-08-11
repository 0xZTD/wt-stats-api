import os
from dotenv import load_dotenv
import requests
import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
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
    await update.message.reply_chat_action(action="typing")

    resp = requests.get(f"{API_URL}/stats", params={"url": chosen})
    resp.raise_for_status()
    results = resp.json()["results"]
    # TODO: add formating
    # Ground, air and naval stats have different fields.
    # general stats same fields, can be reused

    # TODO: make user pick what stats to show
    ground = await format_ground(results["ground_stats"]["ground_realistic"])
    await update.message.reply_text(ground)


async def format_ground(d):
    game_mode = d.get("game_mode", "unknown")
    total_battles = d.get("ground_battles")
    total_targets = d.get("total_targets_destroyed")
    air_targets = d.get("air_targets_destroyed")
    ground_targets = d.get("ground_targets_destroyed")
    naval_targets = d.get("naval_targets_destroyed")

    time_ground = d.get("time_played_ground_battles", "N/A")
    time_tank = d.get("tank_battle_time", "N/A")
    time_td = d.get("tank_destroyer_battle_time", "N/A")
    time_heavy = d.get("heavy_tank_battle_time", "N/A")
    time_spaa = d.get("spaa_battle_time", "N/A")

    battles_tank = d.get("ground_battles_tank")
    battles_spg = d.get("ground_battles_spg")
    battles_heavy = d.get("ground_battles_heavy_tank")
    battles_spaa = d.get("ground_battles_spaa")

    lines = []
    lines.append(f"Mode: {game_mode.capitalize()} (Ground)")
    lines.append("")
    lines.append("General")
    lines.append(f"- Ground battles: {total_battles}")
    lines.append(f"- Time played (ground): {time_ground}")
    lines.append(f"- Targets destroyed: {total_targets}")
    lines.append(f"  -  Air: {air_targets}")
    lines.append(f"  -  Ground: {ground_targets}")
    lines.append(f"  -  Naval: {naval_targets}")
    lines.append("")
    lines.append("By vehicle class")
    lines.append(f"- Tank battles: {battles_tank} | Time: {time_tank}")
    lines.append(f"- Tank destroyer battles: {battles_spg} | Time: {time_td}")
    lines.append(f"- Heavy tank battles: {battles_heavy} | Time: {time_heavy}")
    lines.append(f"- SPAA battles: {battles_spaa} | Time: {time_spaa}")

    return "\n".join(lines)


async def search_nickname(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    nickname = update.message.text.strip()
    await update.message.reply_chat_action(action="typing")
    resp = requests.get(f"{API_URL}/search", params={"q": nickname})
    resp.raise_for_status()
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
        f"Saved {picked_nick}! Use /stats to get your stats.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


async def error_handler(update, context):
    err = context.error
    if isinstance(err, requests.HTTPError):
        resp = err.response
        if resp is not None and resp.status_code in (500, 503):
            if update:
                await update.message.reply_text("⚠️ Resource is busy. Try again later.")
            return

    # Fallback for unexpected errors
    if update:
        update.message.reply_text("❌ An unexpected error occurred.")
    raise


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
    app.add_error_handler(error_handler)
    app.add_handler(CommandHandler("stats", stats))

    app.run_polling()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
