# =============================================================================
# Demo curl requests for Travel DB API
# Base URL: http://localhost:8000
# =============================================================================

BASE_URL="http://localhost:8000"

# =============================================================================
# 1. Users (One-to-Many: User → Trips, User → TravelRequests, User → Messages)
# =============================================================================

# 1.1. Создать пользователя 1
curl -s -X POST "$BASE_URL/api/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "ivan_traveler",
    "email": "ivan@example.com",
    "hashed_password": "securepass123",
    "full_name": "Иван Петров",
    "bio": "Любитель горных путешествий",
    "age": 28,
    "gender": "male",
    "skills": "вождение, фотография, готовка",
    "experience": "5 лет путешествий",
    "preferences": "горы, природа"
  }'
# Ответ: {"id": 1, "username": "ivan_traveler", ...}

# 1.2. Создать пользователя 2
curl -s -X POST "$BASE_URL/api/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "maria_explorer",
    "email": "maria@example.com",
    "hashed_password": "securepass456",
    "full_name": "Мария Сидорова",
    "bio": "Фотограф и путешественница",
    "age": 25,
    "gender": "female",
    "skills": "фотография, видео",
    "experience": "3 года путешествий"
  }'
# Ответ: {"id": 2, "username": "maria_explorer", ...}

# 1.3. Создать пользователя 3
curl -s -X POST "$BASE_URL/api/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alex_adventure",
    "email": "alex@example.com",
    "hashed_password": "securepass789",
    "full_name": "Алексей Козлов",
    "age": 30,
    "gender": "male",
    "skills": "навигация, медицина",
    "experience": "10 лет путешествий"
  }'
# Ответ: {"id": 3, "username": "alex_adventure", ...}

# 1.4. Получить список пользователей
curl -s "$BASE_URL/api/users/?skip=0&limit=10"

# 1.5. Получить пользователя с предпочтительными направлениями
curl -s "$BASE_URL/api/users/1"

# =============================================================================
# 2. Destinations (Many-to-Many: User ↔ Destination, Trip ↔ Destination)
# =============================================================================

# 2.1. Создать направление 1
curl -s -X POST "$BASE_URL/api/destinations/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Байкал",
    "country": "Россия",
    "description": "Глубочайшее озеро в мире",
    "latitude": 53.5,
    "longitude": 107.6
  }'
# Ответ: {"id": 1, "name": "Байкал", "country": "Россия", ...}

# 2.2. Создать направление 2
curl -s -X POST "$BASE_URL/api/destinations/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Камчатка",
    "country": "Россия",
    "description": "Земля вулканов и гейзеров",
    "latitude": 56.0,
    "longitude": 160.5
  }'
# Ответ: {"id": 2, "name": "Камчатка", "country": "Россия", ...}

# 2.3. Создать направление 3
curl -s -X POST "$BASE_URL/api/destinations/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Алтай",
    "country": "Россия",
    "description": "Золотые горы",
    "latitude": 49.4,
    "longitude": 87.0
  }'
# Ответ: {"id": 3, "name": "Алтай", "country": "Россия", ...}

# 2.4. Создать направление 4
curl -s -X POST "$BASE_URL/api/destinations/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Карелия",
    "country": "Россия",
    "description": "Земля озёр и лесов",
    "latitude": 62.0,
    "longitude": 33.0
  }'
# Ответ: {"id": 4, "name": "Карелия", "country": "Россия", ...}

# 2.5. Получить список направлений
curl -s "$BASE_URL/api/destinations/?skip=0&limit=10"

# 2.6. Получить направление с деталями (пользователи и поездки)
curl -s "$BASE_URL/api/destinations/1"

# =============================================================================
# 3. Trips (One-to-Many: User → Trip, Trip → TravelRequests)
#         Many-to-Many: Trip ↔ Destination
# =============================================================================

# 3.1. Создать поездку 1 (creator_id = 1, Иван)
curl -s -X POST "$BASE_URL/api/trips/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Байкальский треккинг",
    "description": "Путешествие вокруг Байкала",
    "start_location": "Улан-Удэ",
    "end_location": "Иркутск",
    "start_date": "2025-07-01",
    "end_date": "2025-07-10",
    "budget": 50000,
    "max_participants": 5,
    "creator_id": 1
  }'
# Ответ: {"id": 1, "title": "Байкальский треккинг", "creator_id": 1, ...}

# 3.2. Создать поездку 2 (creator_id = 2, Мария)
curl -s -X POST "$BASE_URL/api/trips/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Вулканы Камчатки",
    "description": "Покорение вулканов",
    "start_location": "Петропавловск-Камчатский",
    "end_location": "Петропавловск-Камчатский",
    "start_date": "2025-08-15",
    "end_date": "2025-08-25",
    "budget": 120000,
    "max_participants": 4
  }'
# Ответ: {"id": 2, "title": "Вулканы Камчатки", "creator_id": 2, ...}

# 3.3. Создать поездку 3 (creator_id = 3, Алексей)
curl -s -X POST "$BASE_URL/api/trips/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Алтайский маршрут",
    "description": "Треккинг по Алтаю",
    "start_location": "Горно-Алтайск",
    "end_location": "Орток",
    "start_date": "2025-06-15",
    "end_date": "2025-06-25",
    "budget": 40000,
    "max_participants": 6
  }'
# Ответ: {"id": 3, "title": "Алтайский маршрут", "creator_id": 3, ...}

# 3.4. Получить список всех поездок
curl -s "$BASE_URL/api/trips/?skip=0&limit=10"

# 3.5. Получить поездку с деталями (включая направления)
curl -s "$BASE_URL/api/trips/1"

# 3.6. Добавить направление в поездку (Many-to-Many: Trip ↔ Destination)
# Добавляем Байкал (id=1) в поездку "Байкальский треккинг" (id=1)
curl -s -X POST "$BASE_URL/api/trips/1/destinations/1"

# Добавляем Карелию (id=4) в поездку "Байкальский треккинг" (id=1)
curl -s -X POST "$BASE_URL/api/trips/1/destinations/4"

# Добавляем Камчатку (id=2) в поездку "Вулканы Камчатки" (id=2)
curl -s -X POST "$BASE_URL/api/trips/2/destinations/2"

# Добавляем Алтай (id=3) в поездку "Алтайский маршрут" (id=3)
curl -s -X POST "$BASE_URL/api/trips/3/destinations/3"

# Проверить: получить поездку с направлениями
curl -s "$BASE_URL/api/trips/1"

# 3.7. Удалить направление из поездки
curl -s -X DELETE "$BASE_URL/api/trips/1/destinations/4"

# 3.8. Поиск поездок по местам
curl -s "$BASE_URL/api/trips/search?start_location=Улан-Удэ"

# 3.9. Получить активные поездки
curl -s "$BASE_URL/api/trips/active?skip=0&limit=10"

# =============================================================================
# 4. Travel Requests (Many-to-Many: Trip ↔ User через TravelRequest)
#         One-to-Many: Trip → TravelRequest, User → TravelRequest
# =============================================================================

# 4.1. Мария (user_id=2) запрашивает участие в поездке Байкал (trip_id=1)
curl -s -X POST "$BASE_URL/api/travel-requests/" \
  -H "Content-Type: application/json" \
  -d '{
    "trip_id": 1,
    "user_id": 2,
    "message": "Хочу принять участие в Байкальском треккинге!"
  }'
# Ответ: {"id": 1, "trip_id": 1, "user_id": 2, "status": "pending", ...}

# 4.2. Алексей (user_id=3) запрашивает участие в поездке Вулканы Камчатки (trip_id=2)
curl -s -X POST "$BASE_URL/api/travel-requests/" \
  -H "Content-Type: application/json" \
  -d '{
    "trip_id": 2,
    "user_id": 3,
    "message": "Мечтаю покорить вулканы!"
  }'
# Ответ: {"id": 2, "trip_id": 2, "user_id": 3, "status": "pending", ...}

# 4.3. Иван (user_id=1) запрашивает участие в поездке Алтайский маршрут (trip_id=3)
curl -s -X POST "$BASE_URL/api/travel-requests/" \
  -H "Content-Type: application/json" \
  -d '{
    "trip_id": 3,
    "user_id": 1,
    "message": "Отличный маршрут, хочу присоединиться"
  }'
# Ответ: {"id": 3, "trip_id": 3, "user_id": 1, "status": "pending", ...}

# 4.4. Получить запросы для поездки
curl -s "$BASE_URL/api/travel-requests/trip/1"

# 4.5. Получить запросы пользователя
curl -s "$BASE_URL/api/travel-requests/user/2"

# =============================================================================
# 5. Messages (One-to-Many: Trip → Message, User → Message как sender/receiver)
# =============================================================================

# 5.1. Иван (sender_id=1) отправляет сообщение Марии (receiver_id=2) в поездке Байкал (trip_id=1)
curl -s -X POST "$BASE_URL/api/messages/" \
  -H "Content-Type: application/json" \
  -d '{
    "trip_id": 1,
    "sender_id": 1,
    "receiver_id": 2,
    "content": "Привет! Рада, что ты присоединяешься к нашей поездке!"
  }'
# Ответ: {"id": 1, "trip_id": 1, "sender_id": 1, "receiver_id": 2, ...}

# 5.2. Мария (sender_id=2) отвечает Ивану (receiver_id=1)
curl -s -X POST "$BASE_URL/api/messages/" \
  -H "Content-Type: application/json" \
  -d '{
    "trip_id": 1,
    "sender_id": 2,
    "receiver_id": 1,
    "content": "Да! Очень жду не дождусь!"
  }'
# Ответ: {"id": 2, "trip_id": 1, "sender_id": 2, "receiver_id": 1, ...}

# 5.3. Алексей (sender_id=3) отправляет Ивану (receiver_id=1) в поездке Алтай (trip_id=3)
curl -s -X POST "$BASE_URL/api/messages/" \
  -H "Content-Type: application/json" \
  -d '{
    "trip_id": 3,
    "sender_id": 3,
    "receiver_id": 1,
    "content": "Привет! Рад что ты с нами. Подскажи по экипировке."
  }'
# Ответ: {"id": 3, "trip_id": 3, "sender_id": 3, "receiver_id": 1, ...}

# 5.4. Получить сообщения для поездки
curl -s "$BASE_URL/api/messages/trip/1?skip=0&limit=10"

# 5.5. Получить сообщения между пользователями
curl -s "$BASE_URL/api/messages/between?user1_id=1&user2_id=2&trip_id=1&skip=0&limit=10"

# =============================================================================
# 6. Reviews (One-to-Many: User → Review, Trip → Review)
# =============================================================================

# 6.1. Мария (reviewer_id=2) оставляет отзыв Ивану (reviewed_user_id=1) за поездку Байкал (trip_id=1)
curl -s -X POST "$BASE_URL/api/reviews/" \
  -H "Content-Type: application/json" \
  -d '{
    "trip_id": 1,
    "reviewer_id": 2,
    "reviewed_user_id": 1,
    "comment": "Отличный организатор! Всё было супер.",
    "rating": 5
  }'
# Ответ: {"id": 1, "trip_id": 1, "reviewer_id": 2, "reviewed_user_id": 1, "rating": 5, ...}

# 6.2. Алексей (reviewer_id=3) оставляет отзыв Ивану (reviewed_user_id=1) за поездку Алтай (trip_id=3)
curl -s -X POST "$BASE_URL/api/reviews/" \
  -H "Content-Type: application/json" \
  -d '{
    "trip_id": 3,
    "reviewer_id": 3,
    "reviewed_user_id": 1,
    "comment": "Опытный проводник, рекомендую!",
    "rating": 4
  }'
# Ответ: {"id": 2, "trip_id": 3, "reviewer_id": 3, "reviewed_user_id": 1, "rating": 4, ...}

# 6.3. Иван (reviewer_id=1) оставляет отзыв Марии (reviewed_user_id=2) за поездку Вулканы (trip_id=2)
curl -s -X POST "$BASE_URL/api/reviews/" \
  -H "Content-Type: application/json" \
  -d '{
    "trip_id": 2,
    "reviewer_id": 1,
    "reviewed_user_id": 2,
    "comment": "Мария замечательный фотограф и компаньон!",
    "rating": 5
  }'
# Ответ: {"id": 3, "trip_id": 2, "reviewer_id": 1, "reviewed_user_id": 2, "rating": 5, ...}

# 6.4. Получить отзывы для пользователя
curl -s "$BASE_URL/api/reviews/user/1?skip=0&limit=10"

# 6.5. Получить рейтинг пользователя
curl -s "$BASE_URL/api/reviews/user/1/rating"

# =============================================================================
# 7. Health Check
# =============================================================================

curl -s "$BASE_URL/health"

# =============================================================================
# 8. Дополнительно: обновление статуса запроса (TODO - не реализовано)
# =============================================================================

# curl -s -X PATCH "$BASE_URL/api/travel-requests/1" \
#   -H "Content-Type: application/json" \
#   -d '{"status": "accepted"}'

# =============================================================================
# 9. Дополнительно: обновление пользователя
# =============================================================================

curl -s -X PATCH "$BASE_URL/api/users/1" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Иван Петрович Петров",
    "bio": "Опытный путешественник и организатор"
  }'

# =============================================================================
# 10. Дополнительно: обновление направления
# =============================================================================

curl -s -X PATCH "$BASE_URL/api/destinations/1" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Глубочайшее озеро в мире. Объект ЮНЕСКО."
  }'

# =============================================================================
# 11. Дополнительно: удаление (демо)
# =============================================================================

# Удалить поездку (связанные travel_requests и сообщения будут удалены каскадно)
# curl -s -X DELETE "$BASE_URL/api/trips/3"

# Удалить направление
# curl -s -X DELETE "$BASE_URL/api/destinations/4"

# =============================================================================
# 12. Поиск направлений
# =============================================================================

curl -s "$BASE_URL/api/destinations/search?query=Байкал"
