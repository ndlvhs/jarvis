from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os

# Загружаем ключ API OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Определяем модель для запроса
class MessageRequest(BaseModel):
    text: str

@app.post("/process_message")
async def process_message(request: MessageRequest):
    try:
        # Отправляем запрос в OpenAI API
        response = openai.Completion.create(
            model="gpt-4",  # Модель GPT-4 или другая, если нужно
            prompt=request.text,
            max_tokens=150,
            temperature=0.7
        )
        # Возвращаем ответ от OpenAI
        return {"response": response.choices[0].text.strip()}
    except Exception as e:
        return {"error": f"Ошибка при запросе к OpenAI: {str(e)}"}

# Запуск приложения
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)