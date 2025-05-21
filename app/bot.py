# app/bot.py

import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from dotenv import load_dotenv
import requests
from datetime import datetime
import json

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_URL = os.getenv("BACKEND_API_URL")

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler()
async def handle_message(message: types.Message):
    user_text = message.text
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    payload = {
        "text": user_text,
        "now": now_str
    }

    try:
        response = requests.post(API_URL, json=payload)
        data = response.json()

        await message.reply(f"🛠 DEBUG: {data}")

        parsed = data.get("response")
        if isinstance(parsed, str):
            parsed = json.loads(parsed)

        if parsed.get("date") and parsed.get("time"):
            await message.reply(f"✅ Задача: {parsed['task']}\n📅 Когда: {parsed['date']} {parsed['time']}")
        else:
            await message.reply("❌ Не смог распознать дату и время. Попробуй уточнить.")
    except Exception as e:
        await message.reply(f"⚠️ Ошибка: {e}")


# 💡 Новый метод для асинхронного запуска
async def start_bot():
    from asyncio import create_task
    create_task(dp.start_polling())