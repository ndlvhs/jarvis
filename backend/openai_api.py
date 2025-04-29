import openai
import os

# Получаем API ключ из переменной окружения
openai.api_key = os.getenv("OPENAI_API_KEY")

# Пример запроса
response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",  # или gpt-4, если используешь GPT-4
  messages=[
    {"role": "system", "content": "Ты помощник, помогающий с задачами."},
    {"role": "user", "content": "Какой сегодня день?"}
  ]
)

print(response['choices'][0]['message']['content'])

# Пример использования
user_input = "Какой сегодня день?"
response = get_openai_response(user_input)
print(response)