import os
from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv
import requests
from datetime import datetime
import json

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_URL = os.getenv("BACKEND_API_URL")

print(f"🔧 BACKEND_API_URL = {API_URL}")

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

    # Проверим, есть ли API URL
    if not API_URL:
        await message.reply("❌ BACKEND_API_URL не задан!")
        return

    try:
        response = requests.post(API_URL, json=payload, timeout=10)
        response.raise_for_status()  # выбросит ошибку, если код != 200

        data = response.json()
        print(f"📨 Ответ от backend: {data}")
        await message.reply(f"🛠 DEBUG: {data}")

        parsed = data.get("response")
        if isinstance(parsed, str):
            parsed = json.loads(parsed)

        if parsed.get("date") and parsed.get("time"):
            await message.reply(
                f"✅ Задача: {parsed['task']}\n📅 Когда: {parsed['date']} {parsed['time']}"
            )
        else:
            await message.reply("❌ Не смог распознать дату и время. Попробуй уточнить.")
    except Exception as e:
        error_msg = f"⚠️ Ошибка при запросе к API: {e}"
        print(error_msg)
        await message.reply(error_msg)


async def start_bot():
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)