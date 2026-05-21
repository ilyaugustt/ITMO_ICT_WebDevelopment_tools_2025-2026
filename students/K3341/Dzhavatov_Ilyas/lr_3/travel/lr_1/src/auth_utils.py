"""
Модуль для хэширования паролей и работы с JWT токенами.
Реализовано без использования сторонних библиотек.
"""

import base64
import hashlib
import hmac
import json
import secrets
import time
from typing import Optional


def hash_password(password: str) -> str:
    """
    Хэширует пароль с использованием PBKDF2-HMAC-SHA256.
    
    Args:
        password: Пароль в открытом виде
        
    Returns:
        Строка в формате salt:iterations:hash
    """
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
    """
    Проверяет пароль против хэша.
    
    Args:
        password: Пароль в открытом виде
        hashed: Хэш в формате salt:iterations:hash
        
    Returns:
        True если пароль совпадает
    """
    try:
        print(f"PASSWORD {password}")
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


# =============================================================================
# JWT реализация
# =============================================================================


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
    """
    Создаёт JWT токен.
    
    Args:
        payload: Payload токена (dict)
        secret_key: Секретный ключ
        algorithm: Алгоритм подписи (HS256)
        expire_minutes: Время жизни в минутах
        
    Returns:
        JWT токен в виде строки
    """
    header = {
        "alg": algorithm,
        "typ": "JWT"
    }
    
    # Добавляем время истечения
    payload["exp"] = int(time.time()) + expire_minutes * 60
    payload["iat"] = int(time.time())
    
    # Кодируем header и payload
    header_encoded = _base64url_encode(json.dumps(header, separators=(',', ':')).encode('utf-8'))
    payload_encoded = _base64url_encode(json.dumps(payload, separators=(',', ':')).encode('utf-8'))
    
    # Создаём подпись
    signing_input = f"{header_encoded}.{payload_encoded}"
    signature = hmac.new(
        secret_key.encode('utf-8'),
        signing_input.encode('utf-8'),
        hashlib.sha256
    ).digest()
    signature_encoded = _base64url_encode(signature)
    
    return f"{signing_input}.{signature_encoded}"


def decode_jwt(token: str, secret_key: str, algorithm: str = "HS256") -> Optional[dict]:
    """
    Декодирует и проверяет JWT токен.
    
    Args:
        token: JWT токен
        secret_key: Секретный ключ
        algorithm: Алгоритм подписи (HS256)
        
    Returns:
        Payload токена или None если токен невалиден
    """
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return None
        
        header_encoded, payload_encoded, signature_encoded = parts
        
        # Проверяем подпись
        signing_input = f"{header_encoded}.{payload_encoded}"
        expected_signature = hmac.new(
            secret_key.encode('utf-8'),
            signing_input.encode('utf-8'),
            hashlib.sha256
        ).digest()
        expected_signature_encoded = _base64url_encode(expected_signature)
        
        if not hmac.compare_digest(signature_encoded, expected_signature_encoded):
            return None
        
        # Декодируем header и payload
        header = json.loads(_base64url_decode(header_encoded))
        payload = json.loads(_base64url_decode(payload_encoded))
        
        # Проверяем алгоритм
        if header.get("alg") != algorithm:
            return None
        
        # Проверяем время истечения
        exp = payload.get("exp")
        if exp and time.time() > exp:
            return None
        
        return payload
        
    except Exception:
        return None
