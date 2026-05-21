# CRUD операции

## Обзор

Проект использует паттерн Repository для работы с базой данных. Основные CRUD операции инкапсулированы в классах и функциях.

## Класс UserCRUD

### `__init__(self, db: Session)`

Инициализация с сессией базы данных.

### `get_user_by_id(self, user_id: int) -> User | None`

Получение пользователя по ID.

**Параметры:**
- `user_id`: ID пользователя

**Возвращает:** объект `User` или `None`

### `get_user_by_username(self, username: str) -> Optional[User]`

Получение пользователя по имени.

**Параметры:**
- `username`: имя пользователя

**Возвращает:** объект `User` или `None`

### `get_users(self, skip: int = 0, limit: int = 100, active: bool = True) -> list[UserBase]`

Получение списка пользователей.

**Параметры:**
- `skip`: количество пропускаемых записей
- `limit`: максимальное количество записей
- `active`: фильтровать по активности

**Возвращает:** список `UserBase`

### `create_user(self, username, email, hashed_password, **kwargs) -> User`

Создание нового пользователя.

**Параметры:**
- `username`: имя пользователя
- `email`: email
- `hashed_password`: хэш пароля
- `full_name`: полное имя (опционально)
- `bio`: о себе (опционально)
- `age`: возраст (опционально)
- `gender`: пол (опционально)
- `skills`: навыки (опционально)
- `experience`: опыт (опционально)
- `preferences`: предпочтения (опционально)
- `avatar_url`: URL аватара (опционально)

### `update_user(self, user: User, **kwargs) -> User`

Обновление пользователя.

**Параметры:**
- `user`: объект пользователя
- `**kwargs`: поля для обновления

### `deactivate_user(self, user: User) -> User`

Деактивация пользователя.

### `add_preferred_destination(self, user: User, destination: Destination) -> User`

Добавление предпочтительного направления.

### `remove_preferred_destination(self, user: User, destination: Destination) -> User`

Удаление предпочтительного направления.

### `delete_user(self, user: User) -> None`

Удаление пользователя.

### `verify_password(self, user: User, password: str) -> bool`

Проверка пароля.

### `change_password(self, user: User, new_password: str) -> User`

Смена пароля.

## Функции для Trip

### `get_trip_by_id(db, trip_id) -> Trip | None`

Получение поездки по ID с загруженными связями (creator, destinations, travel_requests).

### `get_trips(db, skip=0, limit=100, status=None, creator_id=None) -> list[Trip]`

Получение списка поездок с фильтрацией.

### `get_active_trips_crud(db, skip=0, limit=100) -> list[Trip]`

Получение активных поездок (planned и end_date >= сегодня).

### `search_trips(db, start_location=None, end_location=None, start_date_from=None, start_date_to=None) -> list[Trip]`

Поиск поездок по параметрам.

### `create_trip(db, title, description, start_location, end_location, start_date, end_date, creator_id, **kwargs) -> Trip`

Создание поездки.

### `update_trip(db, trip: Trip, **kwargs) -> Trip`

Обновление поездки.

### `update_trip_status(db, trip: Trip, new_status: str) -> Trip`

Обновление статуса поездки.

### `add_destination_to_trip(db, trip: Trip, destination: Destination) -> Trip`

Добавление направления к поездке.

### `remove_destination_from_trip(db, trip: Trip, destination: Destination) -> Trip`

Удаление направления из поездки.

### `delete_trip(db, trip: Trip) -> None`

Удаление поездки.

## Функции для TravelRequest

### `get_travel_request(db, trip_id, user_id) -> Optional[TravelRequest]`

Получение запроса для поездки и пользователя.

### `get_travel_requests_for_trip(db, trip_id, status=None) -> List[TravelRequest]`

Получение запросов для поездки.

### `get_travel_requests_for_user(db, user_id, status=None) -> List[TravelRequest]`

Получение запросов пользователя.

### `create_travel_request(db, trip_id, user_id, message=None) -> TravelRequest`

Создание запроса на участие.

### `update_travel_request_status(db, request: TravelRequest, new_status: str) -> TravelRequest`

Обновление статуса запроса.

### `delete_travel_request(db, request: TravelRequest) -> None`

Удаление запроса.

## Функции для Destination

### `get_destination_by_id(db, destination_id) -> Optional[Destination]`

Получение направления по ID с загруженными связями.

### `get_destination_by_name(db, name) -> Destination | None`

Получение направления по имени.

### `get_destinations(db, skip=0, limit=100, country=None) -> list[DestinationInDB]`

Получение списка направлений, сортировка по популярности.

### `search_destinations(db, query_text) -> List[Destination]`

Поиск направлений по названию и описанию (ilike).

### `create_destination(db, name, country, description=None, latitude=None, longitude=None) -> Destination`

Создание направления.

### `update_destination(db, destination: Destination, **kwargs) -> Destination`

Обновление направления.

### `update_popularity(db, destination: Destination, increment=True) -> Destination`

Обновление популярности.

### `delete_destination(db, destination: Destination) -> None`

Удаление направления.

## Функции для Message

### `get_message_by_id(db, message_id) -> Optional[Message]`

Получение сообщения по ID с отправителем и получателем.

### `get_messages_for_trip(db, trip_id, skip=0, limit=50) -> List[Message]`

Получение сообщений поездки (сортировка по убыванию created_at).

### `get_messages_between_users(db, user1_id, user2_id, trip_id=None, skip=0, limit=50) -> List[Message]`

Получение сообщений между двумя пользователями.

### `create_message(db, content, trip_id, sender_id, receiver_id) -> Message`

Создание сообщения.

### `delete_message(db, message: Message) -> None`

Удаление сообщения.

## Функции для Review

### `get_review_by_id(db, review_id) -> Optional[Review]`

Получение отзыва по ID с автором, объектом и поездкой.

### `get_reviews_for_user(db, user_id, skip=0, limit=100) -> List[Review]`

Получение отзывов о пользователе.

### `get_reviews_by_reviewer(db, reviewer_id, skip=0, limit=100) -> List[Review]`

Получение отзывов пользователя.

### `get_review_for_trip(db, trip_id, reviewer_id, reviewed_user_id) -> Optional[Review]`

Получение отзыва для конкретной поездки.

### `create_review(db, trip_id, reviewer_id, reviewed_user_id, rating, comment=None) -> Review`

Создание отзыва.

### `update_review(db, review: Review, **kwargs) -> Review`

Обновление отзыва.

### `delete_review(db, review: Review) -> None`

Удаление отзыва.

### `get_user_rating(db, user_id) -> float`

Получение среднего рейтинга пользователя.
