# Модели данных

## Обзор

Проект использует SQLAlchemy ORM для работы с базой данных. Определены 6 основных моделей.

## Базовый класс

```python
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
```

## Enum типы

### TripStatus

Статус поездки:

| Значение | Описание |
|----------|----------|
| `planned` | Запланирована |
| `ongoing` | В процессе |
| `completed` | Завершена |
| `cancelled` | Отменена |

### TravelRequestStatus

Статус запроса на участие:

| Значение | Описание |
|----------|----------|
| `pending` | Ожидает рассмотрения |
| `accepted` | Принят |
| `rejected` | Отклонён |

### Gender

Пол пользователя:

| Значение | Описание |
|----------|----------|
| `male` | Мужской |
| `female` | Женский |
| `other` | Другой |

## Модель User

**Таблица:** `users`

Пользователи системы.

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| `id` | `int` | PK, autoincrement | Идентификатор |
| `username` | `str(50)` | unique, nullable, indexed | Имя пользователя |
| `email` | `str(100)` | unique, nullable, indexed | Email |
| `hashed_password` | `str(255)` | nullable | Хэш пароля |
| `full_name` | `str(100)` | nullable | Полное имя |
| `bio` | `Text` | nullable | О себе |
| `age` | `int` | nullable | Возраст |
| `gender` | `Gender` | nullable | Пол |
| `skills` | `Text` | nullable | Навыки |
| `experience` | `Text` | nullable | Опыт |
| `preferences` | `Text` | nullable | Предпочтения |
| `avatar_url` | `str(255)` | nullable | URL аватара |
| `is_active` | `bool` | default=True | Активность |
| `created_at` | `datetime` | default=now | Дата создания |
| `updated_at` | `datetime` | onupdate=now | Дата обновления |

**Связи:**
- `created_trips` → `Trip` (one-to-many, обратное удаление)
- `travel_requests` → `TravelRequest` (one-to-many, обратное удаление)
- `preferred_destinations` → `Destination` (many-to-many через `user_destinations`)

## Модель Trip

**Таблица:** `trips`

Поездки.

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| `id` | `int` | PK, autoincrement | Идентификатор |
| `title` | `str(100)` | nullable | Название |
| `description` | `Text` | nullable | Описание |
| `start_location` | `str(100)` | nullable | Место начала |
| `end_location` | `str(100)` | nullable | Место окончания |
| `start_date` | `date` | nullable | Дата начала |
| `end_date` | `date` | nullable | Дата окончания |
| `status` | `TripStatus` | default=PLANNED | Статус |
| `budget` | `float` | nullable, >= 0 | Бюджет |
| `max_participants` | `int` | default=10, > 0 | Макс. участников |
| `created_at` | `datetime` | default=now | Дата создания |
| `updated_at` | `datetime` | onupdate=now | Дата обновления |
| `creator_id` | `int` | FK → users.id, nullable, indexed | ID создателя |

**Ограничения таблицы:**
- `ck_trips_dates_valid`: `end_date >= start_date`
- `ck_trips_budget_non_negative`: `budget >= 0`
- `ck_trips_max_participants_positive`: `max_participants > 0`

**Индексы:**
- `ix_trips_dates`: `(start_date, end_date)`
- `ix_trips_locations`: `(start_location, end_location)`

**Связи:**
- `creator` → `User` (many-to-one)
- `destinations` → `Destination` (many-to-many через `trip_destinations`)
- `travel_requests` → `TravelRequest` (one-to-many, обратное удаление)

## Модель TravelRequest

**Таблица:** `travel_requests`

Запросы на участие в поездке.

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| `id` | `int` | PK, autoincrement | Идентификатор |
| `message` | `Text` | nullable | Сообщение |
| `status` | `TravelRequestStatus` | nullable=False, default=PENDING | Статус |
| `created_at` | `datetime` | default=now | Дата создания |
| `updated_at` | `datetime` | onupdate=now | Дата обновления |
| `trip_id` | `int` | FK → trips.id, nullable, indexed | ID поездки |
| `user_id` | `int` | FK → users.id, nullable, indexed | ID пользователя |

**Уникальный индекс:** `ix_travel_requests_trip_user`: `(trip_id, user_id)`

**Связи:**
- `trip` → `Trip` (many-to-one)
- `user` → `User` (many-to-one)

## Модель Destination

**Таблица:** `destinations`

Направления (места назначения).

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| `id` | `int` | PK, autoincrement | Идентификатор |
| `name` | `str(100)` | unique, nullable, indexed | Название |
| `country` | `str(50)` | nullable | Страна |
| `description` | `Text` | nullable | Описание |
| `latitude` | `float` | nullable | Широта |
| `longitude` | `float` | nullable | Долгота |
| `popularity` | `int` | default=0 | Популярность |

**Связи:**
- `interested_users` → `User` (many-to-many через `user_destinations`)
- `trips` → `Trip` (many-to-many через `trip_destinations`)

## Модель Message

**Таблица:** `messages`

Сообщения между пользователями в контексте поездки.

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| `id` | `int` | PK, autoincrement | Идентификатор |
| `content` | `Text` | nullable | Содержание |
| `created_at` | `datetime` | default=now | Дата создания |
| `trip_id` | `int` | FK → trips.id, nullable, indexed | ID поездки |
| `sender_id` | `int` | FK → users.id, nullable, indexed | ID отправителя |
| `receiver_id` | `int` | FK → users.id, nullable, indexed | ID получателя |

**Индекс:** `ix_messages_trip_created`: `(trip_id, created_at)`

**Связи:**
- `trip` → `Trip` (many-to-one)
- `sender` → `User` (many-to-one, foreign_keys=[sender_id])
- `receiver` → `User` (many-to-one, foreign_keys=[receiver_id])

## Модель Review

**Таблица:** `reviews`

Отзывы и рейтинги.

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| `id` | `int` | PK, autoincrement | Идентификатор |
| `comment` | `Text` | nullable | Комментарий |
| `rating` | `int` | nullable=False | Рейтинг |
| `created_at` | `datetime` | default=now | Дата создания |
| `reviewer_id` | `int` | FK → users.id, nullable, indexed | ID автора отзыва |
| `reviewed_user_id` | `int` | FK → users.id, nullable, indexed | ID автора отзыва (о ком) |
| `trip_id` | `int` | FK → trips.id, nullable, indexed | ID поездки |

**Ограничения таблицы:**
- `ck_reviews_rating_valid`: `rating >= 1 AND rating <= 5`

**Уникальный индекс:** `ix_reviews_trip_reviewer`: `(trip_id, reviewer_id)`

**Связи:**
- `reviewer` → `User` (many-to-one, foreign_keys=[reviewer_id])
- `reviewed_user` → `User` (many-to-one, foreign_keys=[reviewed_user_id])
- `trip` → `Trip` (many-to-one)

## Ассоциативные таблицы

### user_destinations

Связь many-to-many между пользователями и направлениями.

| Поле | Тип | Ограничения |
|------|-----|-------------|
| `user_id` | `int` | FK → users.id, PK |
| `destination_id` | `int` | FK → destinations.id, PK |

### trip_destinations

Связь many-to-many между поездками и направлениями.

| Поле | Тип | Ограничения |
|------|-----|-------------|
| `trip_id` | `int` | FK → trips.id, PK |
| `destination_id` | `int` | FK → destinations.id, PK |
