from fastapi import FastAPI
from pydantic import BaseModel
from backend.openai_api import ask_gpt  # Убедись, что путь корректен
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "app"))

from bot import start_bot

# ниже в main.py
import asyncio

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_bot())
app = FastAPI()


class MessageRequest(BaseModel):
    text: str
    now: str


@app.post("/process_message")
async def process_message(req: MessageRequest):
    prompt = (
        f"Сейчас {req.now} (формат ГГГГ-ММ-ДД ЧЧ:ММ, часовой пояс CET). "
        f"Пользователь просит: {req.text}. "
        "Определи дату и время задачи, а также саму задачу. "
        "Верни ответ строго в JSON формате с полями: date, time, task. "
        "Если не понял — верни null."
    )

    result = ask_gpt(prompt)
    return {"response": result}