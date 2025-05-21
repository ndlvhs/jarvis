from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from backend.openai_api import ask_gpt
from datetime import datetime
from app.bot import start_bot  # путь зависит от структуры

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await start_bot()

@app.post("/process_message")
async def process_message(request: Request):
    try:
        data = await request.json()
        text = data.get("text")
        now = data.get("now", datetime.now().strftime("%Y-%m-%d %H:%M"))

        if not text:
            return JSONResponse(content={"error": "Поле 'text' обязательно"}, status_code=400)

        result = ask_gpt(text, now)
        return JSONResponse(content={"response": result})

    except Exception as e:
        return JSONResponse(content={"error": f"Ошибка на сервере: {e}"}, status_code=500)