# War Thunder Stats Telegram Bot

A lightweight Telegram bot for instantly retrieving your personal War Thunder stats.

## What It Does
- Guides you through a quick setup in chat: select your War Thunder profile, and you’re ready.
- Fetches your latest stats from a backend API on request.
- Replies directly in Telegram, making stat-checking fast and easy.

## Tech Stack
- **Python** `python-telegram-bot` for bot logic
- **SQLite** for persisting user profile choices (can swap for another DB)
- **Docker + Docker Compose** for easy multi-service deployment

## Getting Started
1. Get a Telegram bot token from [@BotFather](https://t.me/BotFather).
2. Place your token in a `.env` file as `BOT_TOKEN=...`.
3. Start the services using Docker Compose or run locally.
4. DM the bot `/start` and follow the prompts.

## Commands
- `/start` — Begin setup and pick your War Thunder profile.
- `/stats` — Get your latest stats anytime.

---

This bot was built for fun, learning, and as a portfolio piece showing Python, infra, and Linux skills.  
Feel free to fork or contribute!
