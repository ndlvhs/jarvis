import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_URL = os.getenv("BACKEND_API_URL")  # например: https://jarvis-production-aa5d.up.railway.app/process_message

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

        # если вернулся json с ключами date/time/task — всё ок
        if "response" in data and "date" in data["response"]:
            await message.reply(f"🗓 Задача:\n{data['response']}")
        else:
            await message.reply("❌ Не смог распознать дату и время. Попробуй уточнить.")
    except Exception as e:
        await message.reply(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)