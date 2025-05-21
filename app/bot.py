import os
import requests
import json
from aiogram import Bot, Dispatcher, types
from datetime import datetime

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_URL = os.getenv("BACKEND_API_URL")

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler()
async def handle_message(message: types.Message):
    user_text = message.text
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    payload = {"text": user_text, "now": now_str}

    try:
        response = requests.post(API_URL, json=payload, timeout=10)
        response.raise_for_status()  # выбросит ошибку при статусе != 2xx

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