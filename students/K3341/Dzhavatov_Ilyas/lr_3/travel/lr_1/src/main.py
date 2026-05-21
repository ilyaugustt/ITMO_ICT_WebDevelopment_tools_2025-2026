import fastapi
from fastapi import Depends, HTTPException, Header, status
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.settings import Settings
from src.crud import UserCRUD
from src.models import User
from src.routes import (
    user_router,
    trip_router,
    travel_request_router,
    destination_router,
    message_router,
    review_router,
)
from src.routes.auth import auth_router
from src.connection import get_db


app = fastapi.FastAPI()
settings = Settings()


def create_user_crud(db: Session = Depends(get_db)) -> UserCRUD:
    yield UserCRUD(db)


def get_current_user(
    authorization: str | None = Header(None),
    db: Session = Depends(get_db),
    user_crud: UserCRUD = Depends(create_user_crud),
) -> User:
    """Зависимость для получения текущего пользователя из JWT токена."""
    from src.auth_utils import decode_jwt

    if authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Отсутствует Authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    parts = authorization.split(" ")
    if len(parts) != 2 or parts[0] != "Bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный формат токена. Используйте: Bearer <token>",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = parts[1]
    payload = decode_jwt(token, settings.jwt_secret_key, settings.jwt_algorithm)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный или истёкший токен",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id: int | None = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный токен",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = user_crud.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Пользователь деактивирован",
        )

    return user


# =============================================================================
# Auth Router - /me и /change-password endpoints
# =============================================================================

from fastapi import APIRouter
from src.schemas import UserWithDestinations, UserInDB, PasswordUpdate

auth_extra_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_extra_router.get(
    "/me",
    response_model=UserWithDestinations,
    summary="Получить информацию о текущем пользователе",
)
def get_current_user_info(
    current_user: User = Depends(get_current_user),
):
    """
    Получить информацию о текущем авторизованном пользователе.
    Требует валидный JWT токен.
    """
    return current_user


@auth_extra_router.post(
    "/change-password",
    response_model=UserInDB,
    summary="Сменить пароль",
)
def change_password_endpoint(
    password_data: PasswordUpdate,
    current_user: User = Depends(get_current_user),
    user_crud: UserCRUD = Depends(create_user_crud),
):
    """
    Сменить пароль текущего пользователя.
    Требует валидный JWT токен и старый пароль.
    """
    if not user_crud.verify_password(current_user, password_data.old_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неверный старый пароль",
        )
    return user_crud.change_password(current_user, password_data.new_password)


# Включаем все роуты
app.include_router(user_router, prefix="/api")
app.include_router(trip_router, prefix="/api")
app.include_router(travel_request_router, prefix="/api")
app.include_router(destination_router, prefix="/api")
app.include_router(message_router, prefix="/api")
app.include_router(review_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(auth_extra_router, prefix="/api")


@app.get("/health")
def health_check():
    return {"status": "ok"}
