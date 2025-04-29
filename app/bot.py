import requests
import os
from aiogram import Bot, Dispatcher, types, executor

# Устанавливаем API ключ для Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

# URL API на Railway
API_URL = "https://your-railway-app-url/process_message"

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Привет! Я помогу тебе добавить задачу в календарь. Просто напиши её в свободной форме!")

@dp.message_handler()
async def echo_message(message: types.Message):
    user_text = message.text
    print(f"Received message: {user_text}")

    # Отправляем запрос на новый backend
    response = requests.post(API_URL, json={"text": user_text})
    result = response.json()

    # Отправляем ответ обратно в Telegram
    if "response" in result:
        await message.answer(f"Ответ от OpenAI: {result['response']}")
    else:
        await message.answer("Ошибка при обработке запроса.")

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)