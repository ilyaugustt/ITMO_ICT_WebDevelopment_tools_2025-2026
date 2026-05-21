# Аутентификация

## Обзор

В проекте реализована JWT (JSON Web Token) аутентификация с использованием self-implemented библиотеки. Пароли хэшируются с помощью PBKDF2-HMAC-SHA256.

## Хэширование паролей

### Функция `hash_password()`

Хэширует пароль с использованием PBKDF2-HMAC-SHA256:

```python
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
```

**Параметры:**
- `password`: строка пароля

**Возвращает:** строку в формате `{salt}:{iterations}:{password_hash.hex()}`

### Функция `verify_password()`

Проверяет пароль против хэша:

```python
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
```

**Параметры:**
- `password`: проверяемый пароль
- `hashed`: сохранённый хэш в формате `{salt}:{iterations}:{hash}`

**Возвращает:** `True` если пароль совпадает, иначе `False`

## JWT токены

### Создание токена

```python
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
```

**Структура JWT:**
```
{header}.{payload}.{signature}
```

**Header:**
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

**Payload:**
```json
{
  "sub": "1",
  "exp": 1234567890,
  "iat": 1234567800
}
```

### Декодирование токена

```python
def decode_jwt(token: str, secret_key: str, algorithm: str = "HS256") -> Optional[dict]:
    """Декодирует и проверяет JWT токен."""
    # ...
```

**Проверки при декодировании:**
1. Валидация формата (3 части)
2. Проверка подписи (HMAC-SHA256)
3. Проверка алгоритма
4. Проверка срока действия (exp)

## Зависимость `get_current_user()`

Используется для защиты маршрутов, требующих аутентификации:

```python
def get_current_user(
    authorization: str | None = Header(None),
    db: Session = Depends(get_db),
    user_crud: UserCRUD = Depends(create_user_crud),
) -> User:
```

**Формат заголовка Authorization:**
```
Authorization: Bearer <token>
```

**Возвращаемые ошибки:**

| Код | Описание |
|-----|----------|
| 401 | Отсутствует Authorization header |
| 401 | Неверный формат токена |
| 401 | Недействительный или истёкший токен |
| 401 | Недействительный токен |
| 404 | Пользователь не найден |
| 403 | Пользователь деактивирован |

## Endpoints аутентификации

### POST `/api/auth/login`

Авторизация пользователя, получение JWT токена.

**Request Body:**
```json
{
  "username": "testuser",
  "password": "securepassword123"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

**Response (401):**
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

**Response (200):**
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "full_name": "Test User",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00",
  "preferred_destinations": []
}
```

### POST `/api/auth/change-password`

Смена пароля.

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

## Настройки JWT

В [`settings.py`](setup.md#settingspy):

| Параметр | По умолчанию | Описание |
|----------|--------------|----------|
| `jwt_secret_key` | random (32 bytes) | Секретный ключ подписи |
| `jwt_algorithm` | HS256 | Алгоритм подписи |
| `jwt_expire_minutes` | 30 | Время жизни токена (минуты) |
