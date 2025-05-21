from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
from datetime import datetime
import openai
import json
import asyncio
import sys

# Добавляем app/ в путь, чтобы можно было импортировать bot.py
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "app"))
from bot import start_bot  # функция, запускающая Telegram-бота

load_dotenv()

app = FastAPI()
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.on_event("startup")
async def on_startup():
    print("🚀 Starting FastAPI and Telegram bot...")
    asyncio.create_task(start_bot())


@app.post("/process_message")
async def process_message(request: Request):
    try:
        body = await request.json()
        user_text = body.get("text")
        now = body.get("now")

        print(f"📩 Received message: {user_text}")
        print(f"🕒 Current time: {now}")

        # Отправляем запрос к OpenAI
        prompt = f"""
Ты — помощник, который помогает пользователю распознать задачу и её дату/время.

Сегодня: {now}
Сообщение от пользователя: "{user_text}"

Ответь строго в формате JSON:
{{
    "date": "YYYY-MM-DD",
    "time": "HH:MM",
    "task": "краткое описание задачи"
}}

Если не удалось распознать, верни:
{{ "error": "Ошибка распознавания" }}
"""

        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        result = response.choices[0].message.content.strip()
        print(f"✅ Parsed response: {result}")
        return {"response": result}

    except Exception as e:
        print(f"❌ Ошибка при запросе к OpenAI: {e}")
        return JSONResponse(content={"error": f"Ошибка при запросе к OpenAI: {e}"}, status_code=500)