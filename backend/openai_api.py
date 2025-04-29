import openai

# Убедись, что API-ключ установлен
openai.api_key = "YOUR_API_KEY"

# Отправка запроса с использованием нового интерфейса
def get_openai_response(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Или gpt-4, если ты используешь GPT-4
        messages=[
            {"role": "system", "content": "Ты помощник, помогающий с задачами."},
            {"role": "user", "content": user_input}
        ]
    )
    return response['choices'][0]['message']['content']

# Пример использования
user_input = "Какой сегодня день?"
response = get_openai_response(user_input)
print(response)