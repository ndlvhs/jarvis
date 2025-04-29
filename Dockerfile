# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл requirements.txt из папки backend
COPY backend/requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все остальные файлы
COPY . /app/

# Открываем порт для FastAPI
EXPOSE 8000

# Запускаем приложение
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]