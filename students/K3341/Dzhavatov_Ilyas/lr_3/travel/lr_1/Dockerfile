FROM python:3.11-slim

WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем зависимости
COPY pyproject.toml ./

# Устанавливаем poetry
RUN pip install --no-cache-dir poetry

# Настраиваем poetry и устанавливаем зависимости
RUN poetry install --no-root

COPY migrations migrations
COPY alembic.ini alembic.ini

# Копируем исходный код
COPY . .

# Открываем порт
EXPOSE 8000

COPY entry.sh entry.sh
CMD ["./entry.sh"]