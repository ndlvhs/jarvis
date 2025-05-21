import os
from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv
import requests
from datetime import datetime
import json
import asyncio

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_URL = os.getenv("BACKEND_API_URL")

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

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
            try:
                # Убираем обёртку ```json ... ``` если есть
                parsed_cleaned = parsed.strip()
                if parsed_cleaned.startswith("```json"):
                    parsed_cleaned = parsed_cleaned.removeprefix("```json").removesuffix("```").strip()
                parsed = json.loads(parsed_cleaned)
            except Exception as e:
                await message.reply(f"⚠️ Ошибка при парсинге ответа: {e}")
                return

        if parsed.get("date") and parsed.get("time"):
            await message.reply(f"✅ Задача: {parsed['task']}\n📅 Когда: {parsed['date']} {parsed['time']}")
        else:
            await message.reply("❌ Не смог распознать дату и время. Попробуй уточнить.")
    except Exception as e:
        await message.reply(f"⚠️ Ошибка: {e}")

# 👇 Запускаем бота асинхронно, совместимо с FastAPI
async def start_bot():
    asyncio.create_task(dp.start_polling())