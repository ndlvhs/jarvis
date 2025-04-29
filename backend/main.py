import openai
import os
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные окружения

# Устанавливаем ключ API OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

@app.post("/process_message")
async def process_message(text: str):
    try:
        # Запрос к OpenAI API
        response = openai.completions.create(
            model="gpt-4",  # Используем модель GPT-4
            prompt=text,
            max_tokens=150,
            temperature=0.7
        )
        # Возвращаем результат
        return {"response": response.choices[0].text.strip()}
    except Exception as e:
        return {"error": f"Ошибка при запросе к OpenAI: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)