# Используем базовый образ Python 3.10
FROM python:3.10


# Установка рабочей директории внутри контейнера
WORKDIR /app

# Копирование файлов для установки зависимостей через Poetry
COPY pyproject.toml poetry.lock /app/
COPY . /app

# Установка зависимостей через Poetry
RUN apt-get update && apt-get install -y make
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

# Определение порта, который будет использоваться вашим приложением
EXPOSE 8000

# Команда для запуска приложения при старте контейнера
CMD ["make", "start"]
