# Установка и запуск

## Требования

- Python 3.10+
- PostgreSQL 14+

## Установка

### 1. Клонирование репозитория

```bash
git clone https://github.com/username/repo.git
cd repo/lr_1
```

### 2. Установка зависимостей

Проект использует `poetry` для управления зависимостями.

```bash
# Установка poetry (если не установлен)
pip install poetry

# Установка зависимостей проекта
poetry install
```

Или с использованием pip:

```bash
pip install -e .
```

### 3. Настройка базы данных

Создайте базу данных PostgreSQL:

```sql
CREATE DATABASE travel;
CREATE USER travel_user WITH PASSWORD 'travel_password';
GRANT ALL PRIVILEGES ON DATABASE travel TO travel_user;
```

### 4. Настройка переменных окружения

Создайте файл `.env` на основе шаблона:

```bash
cp .env.example .env
```

Содержимое файла `.env`:

```env
DATABASE_URL=postgresql://travel_user:travel_password@localhost:5432/travel
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=30
```

### 5. Применение миграций

```bash
# Использование Makefile
make alembic-upgrade-head

# Или напрямую
poetry run alembic upgrade head
```

## Запуск

### Режим разработки

```bash
# Использование Makefile
make run

# Или напрямую
poetry run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Сервер запустится по адресу: `http://localhost:8000`

### API документация

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Проверка состояния

```bash
curl http://localhost:8000/health
```

## Тестирование API

### Регистрация пользователя

```bash
curl -X POST "http://localhost:8000/api/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepassword123",
    "full_name": "Test User"
  }'
```

### Авторизация

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "securepassword123"
  }'
```

### Получение информации о текущем пользователе

```bash
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer <your_jwt_token>"
```

## Управление миграциями

### Создание новой миграции

```bash
# Использование Makefile
make alembic-auto-revision message="описание изменений"

# Или напрямую
poetry run alembic revision --autogenerate -m "описание изменений"
```

### Применение миграций

```bash
poetry run alembic upgrade head
```

### Откат миграции

```bash
poetry run alembic downgrade -1
```

## Структура конфигурации

### pyproject.toml

Описывает зависимости проекта и настройки сборки.

### Makefile

Содержит полезные команды для работы с проектом:

| Команда | Описание |
|---------|----------|
| `make alembic-upgrade-head` | Применить миграции до head |
| `make alembic-auto-revision message="..."` | Создать авто-ревизию миграции |

### connection.py

Подключение к базе данных:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.settings import settings

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

### settings.py

Настройки приложения:

```python
from pydantic_settings import BaseSettings, SettingsConfigDict
import secrets

class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@localhost/travel"
    jwt_secret_key: str = secrets.token_urlsafe(32)
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30

    model_config = SettingsConfigDict(env_file=".env")
```
