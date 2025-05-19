from fastapi import FastAPI
from pydantic import BaseModel
from openai_api import ask_gpt  # импортируем функцию, обращающуюся к OpenAI
import logging

app = FastAPI()

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Модель запроса
class MessageRequest(BaseModel):
    text: str
    now: str  # формат: '2025-04-29 10:23'

@app.post("/process_message")
async def process_message(request: MessageRequest):
    prompt = f"Сейчас {request.now}. Пользователь написал: \"{request.text}\". Выдели из этого дату, время и задачу. Ответ верни в JSON-формате с полями date, time и task. Если не получилось — напиши 'null'."

    logging.info(f"Prompt sent to GPT: {prompt}")

    try:
        gpt_response = ask_gpt(prompt)
        logging.info(f"GPT response: {gpt_response}")
        return {"response": gpt_response}
    except Exception as e:
        logging.error(f"OpenAI error: {e}")
        return {"error": f"Ошибка при обращении к OpenAI: {str(e)}"}