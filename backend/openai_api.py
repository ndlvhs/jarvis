import os
import openai

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_gpt(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # или "gpt-4" если используешь его
            messages=[
                {"role": "system", "content": "Ты ассистент, помогающий выделять дату, время и задачу. Отвечай строго в JSON с полями: date, time, task. Если не понял — верни null."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Ошибка при запросе к OpenAI: {str(e)}"