import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_gpt(text: str, now: str) -> str:
    try:
        prompt = (
            f"Сегодня: {now}\n"
            f"Пользователь написал: '{text}'\n"
            "Извлеки из этого задачи в формате JSON:\n"
            "{ \"date\": \"YYYY-MM-DD\", \"time\": \"HH:MM\", \"task\": \"...\" }"
        )

        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Ты помощник по планированию задач. Всегда возвращай JSON с датой, временем и задачей."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Ошибка при запросе к OpenAI: {e}"