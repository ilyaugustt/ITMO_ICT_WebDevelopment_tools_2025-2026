# API Endpoints

## Auth

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/login` | Авторизация, получение JWT токена | Нет |
| GET | `/api/auth/me` | Информация о текущем пользователе | Да |
| POST | `/api/auth/change-password` | Смена пароля | Да |

### POST `/api/auth/login`

Авторизация пользователя по username и password. Возвращает JWT токен.

**Request Body:**
```json
{
  "username": "testuser",
  "password": "securepassword123"
}
```

**Response 200 OK:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

**Response 401 Unauthorized:**
```json
{
  "detail": "Неверное имя пользователя или пароль"
}
```

### GET `/api/auth/me`

Получение информации о текущем пользователе.

**Headers:**
```
Authorization: Bearer <token>
```

**Response 200 OK:**
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "full_name": "Test User",
  "bio": "Test bio",
  "age": 25,
  "gender": "male",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00",
  "preferred_destinations": []
}
```

### POST `/api/auth/change-password`

Смена пароля аутентифицированного пользователя.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "old_password": "securepassword123",
  "new_password": "newsecurepassword456"
}
```

---

## Users

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/users/` | Регистрация нового пользователя | Нет |
| GET | `/api/users/` | Список пользователей | Нет |
| GET | `/api/users/{user_id}` | Информация о пользователе | Нет |
| PATCH | `/api/users/{user_id}` | Обновление пользователя | Нет |
| DELETE | `/api/users/{user_id}` | Удаление пользователя | Нет |

### POST `/api/users/`

Регистрация нового пользователя.

**Request Body:**
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "securepassword123",
  "full_name": "Test User",
  "bio": "Test bio",
  "age": 25,
  "gender": "male"
}
```

**Response 201 Created:**
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "full_name": "Test User",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00"
}
```

**Response 400 Bad Request:**
```json
{
  "detail": "Username уже занят"
}
```

### GET `/api/users/`

Получение списка пользователей.

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| active | bool | True | Фильтр по активности |

**Response 200 OK:**
```json
[
  {
    "username": "testuser",
    "email": "test@example.com",
    "full_name": "Test User"
  }
]
```

### GET `/api/users/{user_id}`

Получение информации о конкретном пользователе.

**Response 200 OK:**
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "full_name": "Test User",
  "preferred_destinations": [
    {
      "id": 1,
      "name": "Paris",
      "country": "France"
    }
  ]
}
```

### PATCH `/api/users/{user_id}`

Обновление информации о пользователе.

**Request Body:**
```json
{
  "full_name": "Updated Name",
  "bio": "Updated bio"
}
```

### DELETE `/api/users/{user_id}`

Удаление пользователя.

**Response 204 No Content**

---

## Trips

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

### POST `/api/trips/`

Создание новой поездки.

**Request Body:**
```json
{
  "title": "Trip to Paris",
  "description": "Amazing trip",
  "start_location": "Moscow",
  "end_location": "Paris",
  "start_date": "2024-06-01",
  "end_date": "2024-06-10",
  "budget": 1000.0,
  "max_participants": 10
}
```

### GET `/api/trips/`

Получение списка всех поездок.

### GET `/api/trips/active`

Получение списка активных поездок (planned или ongoing).

### GET `/api/trips/search`

Поиск поездок по параметрам.

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| start_location | str | Место начала |
| end_location | str | Место окончания |
| start_date | date | Дата начала |
| end_date | date | Дата окончания |

### GET `/api/trips/{trip_id}`

Получение информации о конкретной поездке.

**Response 200 OK:**
```json
{
  "id": 1,
  "title": "Trip to Paris",
  "description": "Amazing trip",
  "start_location": "Moscow",
  "end_location": "Paris",
  "start_date": "2024-06-01",
  "end_date": "2024-06-10",
  "status": "planned",
  "budget": 1000.0,
  "max_participants": 10,
  "destinations": [
    {
      "id": 1,
      "name": "Eiffel Tower",
      "country": "France"
    }
  ]
}
```

### PATCH `/api/trips/{trip_id}`

Обновление поездки.

**Request Body:**
```json
{
  "title": "Updated Trip Title",
  "status": "ongoing"
}
```

### POST `/api/trips/{trip_id}/destinations/{destination_id}`

Добавление направления к поездке.

**Response 201 Created**

### DELETE `/api/trips/{trip_id}/destinations/{destination_id}`

Удаление направления из поездки.

**Response 204 No Content**

### DELETE `/api/trips/{trip_id}`

Удаление поездки.

**Response 204 No Content**

---

## Destinations

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/destinations/` | Создать направление | Нет |
| GET | `/api/destinations/` | Список направлений | Нет |
| GET | `/api/destinations/search` | Поиск направлений | Нет |
| GET | `/api/destinations/{destination_id}` | Информация о направлении | Нет |
| PATCH | `/api/destinations/{destination_id}` | Обновить направление | Нет |
| POST | `/api/destinations/{destination_id}/popularity` | Обновить популярность | Нет |
| DELETE | `/api/destinations/{destination_id}` | Удалить направление | Нет |

### POST `/api/destinations/`

Создание нового направления.

**Request Body:**
```json
{
  "name": "Paris",
  "country": "France",
  "description": "City of Light",
  "latitude": 48.8566,
  "longitude": 2.3522
}
```

### GET `/api/destinations/search`

Поиск направлений.

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| name | str | Название (частичное совпадение) |
| country | str | Страна |

### PATCH `/api/destinations/{destination_id}`

Обновление направления.

### POST `/api/destinations/{destination_id}/popularity`

Обновление популярности направления.

**Request Body:**
```json
{
  "popularity_delta": 1
}
```

---

## Travel Requests

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/travel-requests/` | Создать запрос на участие | Нет |
| GET | `/api/travel-requests/trip/{trip_id}` | Запросы для поездки | Нет |
| GET | `/api/travel-requests/user/{user_id}` | Запросы пользователя | Нет |
| PATCH | `/api/travel-requests/{request_id}` | Обновить статус запроса | Нет |

### POST `/api/travel-requests/`

Создание запроса на участие в поездке.

**Request Body:**
```json
{
  "trip_id": 1,
  "user_id": 2,
  "message": "I would like to join this trip"
}
```

### GET `/api/travel-requests/trip/{trip_id}`

Получение всех запросов для конкретной поездки.

### GET `/api/travel-requests/user/{user_id}`

Получение всех запросов конкретного пользователя.

### PATCH `/api/travel-requests/{request_id}`

Обновление статуса запроса.

**Request Body:**
```json
{
  "status": "accepted"
}
```

---

## Messages

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/messages/` | Создать сообщение | Нет |
| GET | `/api/messages/trip/{trip_id}` | Сообщения поездки | Нет |
| GET | `/api/messages/between` | Сообщения между пользователями | Нет |

### POST `/api/messages/`

Создание сообщения.

**Request Body:**
```json
{
  "trip_id": 1,
  "sender_id": 1,
  "receiver_id": 2,
  "content": "Hello! Are you joining the trip?"
}
```

### GET `/api/messages/trip/{trip_id}`

Получение всех сообщений для поездки.

### GET `/api/messages/between`

Получение сообщений между двумя пользователями.

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| trip_id | int | ID поездки |
| user1_id | int | ID первого пользователя |
| user2_id | int | ID второго пользователя |

---

## Reviews

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/reviews/` | Создать отзыв | Нет |
| GET | `/api/reviews/user/{user_id}` | Отзывы о пользователе | Нет |
| GET | `/api/reviews/user/{user_id}/rating` | Рейтинг пользователя | Нет |
| DELETE | `/api/reviews/{review_id}` | Удалить отзыв | Нет |

### POST `/api/reviews/`

Создание отзыва.

**Request Body:**
```json
{
  "trip_id": 1,
  "reviewer_id": 1,
  "reviewed_user_id": 2,
  "rating": 5,
  "comment": "Great travel companion!"
}
```

**Response 400 Bad Request:**
```json
{
  "detail": "Rating must be between 1 and 5"
}
```

### GET `/api/reviews/user/{user_id}`

Получение всех отзывов о пользователе.

### GET `/api/reviews/user/{user_id}/rating`

Получение среднего рейтинга пользователя.

**Response 200 OK:**
```json
{
  "user_id": 1,
  "average_rating": 4.5,
  "review_count": 10
}
```

### DELETE `/api/reviews/{review_id}`

Удаление отзыва.

**Response 204 No Content**

---

## Health

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Проверка состояния приложения |

### GET `/health`

**Response 200 OK:**
```json
{
  "status": "ok"
}
```
