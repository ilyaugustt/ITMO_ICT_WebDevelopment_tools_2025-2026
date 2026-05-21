# Лабораторная работа №1 — Travel API

## Описание

FastAPI приложение для управления путешествиями. Реализована система авторизации с JWT-токенами, CRUD операции для пользователей, поездок, направлений, запросов на участие, сообщений и отзывов.

## Структура проекта

```
lr_1/
├── src/
│   ├── __init__.py
│   ├── main.py              # Точка входа приложения
│   ├── models.py            # SQLAlchemy модели
│   ├── schemas.py           # Pydantic схемы
│   ├── settings.py          # Настройки приложения
│   ├── crud.py              # CRUD операции с БД
│   ├── auth_utils.py        # Хэширование и JWT
│   ├── connection.py        # Подключение к БД
│   └── routes/              # Роуты
│       ├── __init__.py
│       ├── auth.py          # Авторизация
│       ├── users.py         # Пользователи
│       ├── trips.py         # Поездки
│       ├── travel_requests.py # Запросы на участие
│       ├── destinations.py  # Направления
│       ├── messages.py      # Сообщения
│       └── reviews.py       # Отзывы
├── migrations/              # Alembic миграции
├── pyproject.toml           # Зависимости
└── README.md                # Этот файл
```

## Установка и запуск

### Зависимости

- Python 3.10+
- PostgreSQL

### Установка

```bash
cd lr_1
pip install -e .
```

### Запуск

```bash
uvicorn src.main:app --reload
```

API документация: http://localhost:8000/docs

---

## Соединение с базой данных

### Файл: `src/connection.py`

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.settings import settings

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

### Файл: `src/settings.py`

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

### Функция получения сессии БД:

```python
from src.connection import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

## Модели данных

### Файл: `src/models.py`

```python
from sqlalchemy import (
    Column, Integer, String, Float, Date, DateTime,
    Boolean, Enum, ForeignKey, Table, Text,
    CheckConstraint, Index,
)
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from datetime import datetime, date
from typing import Optional
import enum


class Base(DeclarativeBase):
    pass


# =============================================================================
# Enum для типов данных
# =============================================================================

class TripStatus(str, enum.Enum):
    PLANNED = "planned"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TravelRequestStatus(str, enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


# =============================================================================
# Ассоциативные таблицы
# =============================================================================

user_destinations = Table(
    "user_destinations",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("destination_id", Integer, ForeignKey("destinations.id", ondelete="CASCADE"), primary_key=True),
)

trip_destinations = Table(
    "trip_destinations",
    Base.metadata,
    Column("trip_id", Integer, ForeignKey("trips.id", ondelete="CASCADE"), primary_key=True),
    Column("destination_id", Integer, ForeignKey("destinations.id", ondelete="CASCADE"), primary_key=True),
)


# =============================================================================
# Таблица 1: Users
# =============================================================================

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(100))
    bio: Mapped[Optional[str]] = mapped_column(Text)
    age: Mapped[Optional[int]] = mapped_column(Integer)
    gender: Mapped[Optional[Gender]] = mapped_column(Enum(Gender))
    skills: Mapped[Optional[str]] = mapped_column(Text)
    experience: Mapped[Optional[str]] = mapped_column(Text)
    preferences: Mapped[Optional[str]] = mapped_column(Text)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    created_trips: Mapped[list["Trip"]] = relationship(back_populates="creator", cascade="all, delete-orphan")
    travel_requests: Mapped[list["TravelRequest"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    preferred_destinations: Mapped[list["Destination"]] = relationship(
        secondary=user_destinations, back_populates="interested_users"
    )


# =============================================================================
# Таблица 2: Trips
# =============================================================================

class Trip(Base):
    __tablename__ = "trips"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    start_location: Mapped[str] = mapped_column(String(100), nullable=False)
    end_location: Mapped[str] = mapped_column(String(100), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[TripStatus] = mapped_column(Enum(TripStatus), default=TripStatus.PLANNED)
    budget: Mapped[Optional[float]] = mapped_column(Float)
    max_participants: Mapped[int] = mapped_column(Integer, default=10)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)
    creator_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    creator: Mapped["User"] = relationship(back_populates="created_trips")
    destinations: Mapped[list["Destination"]] = relationship(
        secondary=trip_destinations, back_populates="trips"
    )
    travel_requests: Mapped[list["TravelRequest"]] = relationship(back_populates="trip", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("end_date >= start_date", name="ck_trips_dates_valid"),
        CheckConstraint("budget >= 0", name="ck_trips_budget_non_negative"),
        CheckConstraint("max_participants > 0", name="ck_trips_max_participants_positive"),
        Index("ix_trips_dates", "start_date", "end_date"),
        Index("ix_trips_locations", "start_location", "end_location"),
    )


# =============================================================================
# Таблица 3: TravelRequests
# =============================================================================

class TravelRequest(Base):
    __tablename__ = "travel_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    message: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[TravelRequestStatus] = mapped_column(
        Enum(TravelRequestStatus), default=TravelRequestStatus.PENDING, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)
    trip_id: Mapped[int] = mapped_column(Integer, ForeignKey("trips.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    trip: Mapped["Trip"] = relationship(back_populates="travel_requests")
    user: Mapped["User"] = relationship(back_populates="travel_requests")

    __table_args__ = (
        Index("ix_travel_requests_trip_user", "trip_id", "user_id", unique=True),
    )


# =============================================================================
# Таблица 4: Destinations
# =============================================================================

class Destination(Base):
    __tablename__ = "destinations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    country: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    latitude: Mapped[Optional[float]] = mapped_column(Float)
    longitude: Mapped[Optional[float]] = mapped_column(Float)
    popularity: Mapped[int] = mapped_column(Integer, default=0)

    interested_users: Mapped[list["User"]] = relationship(
        secondary=user_destinations, back_populates="preferred_destinations"
    )
    trips: Mapped[list["Trip"]] = relationship(secondary=trip_destinations, back_populates="destinations")


# =============================================================================
# Таблица 5: Messages
# =============================================================================

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    trip_id: Mapped[int] = mapped_column(Integer, ForeignKey("trips.id", ondelete="CASCADE"), nullable=False, index=True)
    sender_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    receiver_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    trip: Mapped["Trip"] = relationship()
    sender: Mapped["User"] = relationship(foreign_keys=[sender_id])
    receiver: Mapped["User"] = relationship(foreign_keys=[receiver_id])

    __table_args__ = (Index("ix_messages_trip_created", "trip_id", "created_at"),)


# =============================================================================
# Таблица 6: Reviews
# =============================================================================

class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    comment: Mapped[Optional[str]] = mapped_column(Text)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    reviewer_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    reviewed_user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    trip_id: Mapped[int] = mapped_column(Integer, ForeignKey("trips.id", ondelete="CASCADE"), nullable=False, index=True)

    reviewer: Mapped["User"] = relationship(foreign_keys=[reviewer_id])
    reviewed_user: Mapped["User"] = relationship(foreign_keys=[reviewed_user_id])
    trip: Mapped["Trip"] = relationship()

    __table_args__ = (
        CheckConstraint("rating >= 1 AND rating <= 5", name="ck_reviews_rating_valid"),
        Index("ix_reviews_trip_reviewer", "trip_id", "reviewer_id", unique=True),
    )
```

---

## Аутентификация

### Файл: `src/auth_utils.py`

```python
import base64
import hashlib
import hmac
import json
import secrets
import time
from typing import Optional


def hash_password(password: str) -> str:
    """Хэширует пароль с использованием PBKDF2-HMAC-SHA256."""
    salt = secrets.token_hex(16)
    iterations = 100000
    password_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        iterations
    )
    return f"{salt}:{iterations}:{password_hash.hex()}"


def verify_password(password: str, hashed: str) -> bool:
    """Проверяет пароль против хэша."""
    try:
        salt, iterations, password_hash = hashed.split(':')
        iterations = int(iterations)
        computed_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            iterations
        )
        return hmac.compare_digest(computed_hash.hex(), password_hash)
    except (ValueError, AttributeError):
        return False


def _base64url_encode(data: bytes) -> str:
    """Кодирует байты в base64url без padding."""
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')


def _base64url_decode(s: str) -> bytes:
    """Декодирует base64url строку в байты."""
    padding = 4 - len(s) % 4
    if padding != 4:
        s += '=' * padding
    return base64.urlsafe_b64decode(s)


def create_jwt(payload: dict, secret_key: str, algorithm: str = "HS256", expire_minutes: int = 30) -> str:
    """Создаёт JWT токен."""
    header = {"alg": algorithm, "typ": "JWT"}
    payload["exp"] = int(time.time()) + expire_minutes * 60
    payload["iat"] = int(time.time())

    header_encoded = _base64url_encode(json.dumps(header, separators=(',', ':')).encode('utf-8'))
    payload_encoded = _base64url_encode(json.dumps(payload, separators=(',', ':')).encode('utf-8'))

    signing_input = f"{header_encoded}.{payload_encoded}"
    signature = hmac.new(
        secret_key.encode('utf-8'),
        signing_input.encode('utf-8'),
        hashlib.sha256
    ).digest()
    signature_encoded = _base64url_encode(signature)

    return f"{signing_input}.{signature_encoded}"


def decode_jwt(token: str, secret_key: str, algorithm: str = "HS256") -> Optional[dict]:
    """Декодирует и проверяет JWT токен."""
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return None

        header_encoded, payload_encoded, signature_encoded = parts

        signing_input = f"{header_encoded}.{payload_encoded}"
        expected_signature = hmac.new(
            secret_key.encode('utf-8'),
            signing_input.encode('utf-8'),
            hashlib.sha256
        ).digest()
        expected_signature_encoded = _base64url_encode(expected_signature)

        if not hmac.compare_digest(signature_encoded, expected_signature_encoded):
            return None

        header = json.loads(_base64url_decode(header_encoded))
        payload = json.loads(_base64url_decode(payload_encoded))

        if header.get("alg") != algorithm:
            return None

        exp = payload.get("exp")
        if exp and time.time() > exp:
            return None

        return payload
    except Exception:
        return None
```

---

## API Endpoints

### Auth

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/login` | Авторизация, получение JWT токена | Нет |
| GET | `/api/auth/me` | Информация о текущем пользователе | Да |
| POST | `/api/auth/change-password` | Смена пароля | Да |

### Users

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/users/` | Регистрация нового пользователя | Нет |
| GET | `/api/users/` | Список пользователей | Нет |
| GET | `/api/users/{user_id}` | Информация о пользователе | Нет |
| PATCH | `/api/users/{user_id}` | Обновление пользователя | Нет |
| DELETE | `/api/users/{user_id}` | Удаление пользователя | Нет |

### Trips

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/trips/` | Создать поездку | Нет |
| GET | `/api/trips/` | Список поездок | Нет |
| GET | `/api/trips/active` | Активные поездки | Нет |
| GET | `/api/trips/search` | Поиск поездок | Нет |
| GET | `/api/trips/{trip_id}` | Информация о поездке | Нет |
| PATCH | `/api/trips/{trip_id}` | Обновить поездку | Нет |
| POST | `/api/trips/{trip_id}/destinations/{destination_id}` | Добавить направление | Нет |
| DELETE | `/api/trips/{trip_id}/destinations/{destination_id}` | Удалить направление | Нет |
| DELETE | `/api/trips/{trip_id}` | Удалить поездку | Нет |

### Destinations

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/destinations/` | Создать направление | Нет |
| GET | `/api/destinations/` | Список направлений | Нет |
| GET | `/api/destinations/search` | Поиск направлений | Нет |
| GET | `/api/destinations/{destination_id}` | Информация о направлении | Нет |
| PATCH | `/api/destinations/{destination_id}` | Обновить направление | Нет |
| POST | `/api/destinations/{destination_id}/popularity` | Обновить популярность | Нет |
| DELETE | `/api/destinations/{destination_id}` | Удалить направление | Нет |

### Travel Requests

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/travel-requests/` | Создать запрос на участие | Нет |
| GET | `/api/travel-requests/trip/{trip_id}` | Запросы для поездки | Нет |
| GET | `/api/travel-requests/user/{user_id}` | Запросы пользователя | Нет |
| PATCH | `/api/travel-requests/{request_id}` | Обновить статус запроса | Нет |

### Messages

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/messages/` | Создать сообщение | Нет |
| GET | `/api/messages/trip/{trip_id}` | Сообщения поездки | Нет |
| GET | `/api/messages/between` | Сообщения между пользователями | Нет |

### Reviews

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/reviews/` | Создать отзыв | Нет |
| GET | `/api/reviews/user/{user_id}` | Отзывы о пользователе | Нет |
| GET | `/api/reviews/user/{user_id}/rating` | Рейтинг пользователя | Нет |
| DELETE | `/api/reviews/{review_id}` | Удалить отзыв | Нет |

### Health

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Проверка состояния приложения |

---

## Схемы данных

### Файл: `src/schemas.py`

```python
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime, date
from enum import Enum
from pydantic_settings import SettingsConfigDict


class TripStatusEnum(str, Enum):
    PLANNED = "planned"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TravelRequestStatusEnum(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class GenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore")
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(..., max_length=100)
    full_name: str | None = Field(None, max_length=100)
    bio: str | None = None
    age: int | None = None
    gender: GenderEnum | None = None
    skills: str | None = None
    experience: str | None = None
    preferences: str | None = None
    avatar_url: str | None = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=255)


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, max_length=100)
    bio: str | None = None
    age: int | None = None
    gender: GenderEnum | None = None
    skills: str | None = None
    experience: str | None = None
    preferences: str | None = None
    avatar_url: str | None = None


class UserInDB(UserBase):
    id: int
    is_active: bool = True
    created_at: datetime
    updated_at: datetime | None = None
    model_config = SettingsConfigDict(from_attributes=True)


class UserWithDestinations(UserInDB):
    preferred_destinations: Optional[List["DestinationInDB"]] = None


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=1, max_length=255)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class PasswordUpdate(BaseModel):
    old_password: str = Field(..., min_length=1, max_length=255)
    new_password: str = Field(..., min_length=8, max_length=255)
```

---

## CRUD операции

### Файл: `src/crud.py`

```python
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import Optional, List
from datetime import datetime
from .models import User, Trip, TravelRequest, Destination, Message, Review
from .schemas import UserBase, DestinationInDB, TripInDB


class UserCRUD:
    def __init__(self, db: Session):
        self._db = db

    def get_user_by_id(self, user_id: int) -> User | None:
        return self._db.query(User).filter(User.id == user_id).first()

    def get_user_by_username(self, username: str) -> Optional[User]:
        return self._db.query(User).filter(User.username == username).first()

    def get_users(self, skip: int = 0, limit: int = 100, active: bool = True) -> list[UserBase]:
        query = self._db.query(User)
        if active:
            query = query.filter(User.is_active == True)
        users = query.offset(skip).limit(limit).all()
        return [UserBase.model_validate(user) for user in users]

    def create_user(
        self, username: str, email: str, hashed_password: str,
        full_name: Optional[str] = None, bio: Optional[str] = None,
        age: Optional[int] = None, gender: Optional[str] = None,
        skills: Optional[str] = None, experience: Optional[str] = None,
        preferences: Optional[str] = None, avatar_url: Optional[str] = None,
    ) -> User:
        user = User(
            username=username, email=email, hashed_password=hashed_password,
            full_name=full_name, bio=bio, age=age, gender=gender,
            skills=skills, experience=experience, preferences=preferences,
            avatar_url=avatar_url,
        )
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)
        return user

    def update_user(self, user: User, **kwargs) -> User:
        for key, value in kwargs.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)
        self._db.commit()
        self._db.refresh(user)
        return user

    def verify_password(self, user: User, password: str) -> bool:
        from src.auth_utils import verify_password as verify
        return verify(password, user.hashed_password)

    def change_password(self, user: User, new_password: str) -> User:
        from src.auth_utils import hash_password
        user.hashed_password = hash_password(new_password)
        self._db.commit()
        self._db.refresh(user)
        return user
```

---

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

### Получение JWT токена

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

### Смена пароля

```bash
curl -X POST "http://localhost:8000/api/auth/change-password" \
  -H "Authorization: Bearer <your_jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "old_password": "securepassword123",
    "new_password": "newsecurepassword456"
  }'
```
