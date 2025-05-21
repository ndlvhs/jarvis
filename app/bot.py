import os
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from dotenv import load_dotenv
from datetime import datetime

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

        # DEBUG: временно выводим весь ответ сервера
        await message.reply(f"🛠 DEBUG: {data}")

        parsed = data.get("response")
        if isinstance(parsed, str):
            import json
            parsed = json.loads(parsed)

        if parsed and parsed.get("date") and parsed.get("time"):
            await message.reply(f"✅ Задача: {parsed['task']}\n📅 Когда: {parsed['date']} {parsed['time']}")
        else:
            await message.reply("❌ Не смог распознать дату и время. Попробуй уточнить.")
    except Exception as e:
        await message.reply(f"⚠️ Ошибка при обращении к API: {e}")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)