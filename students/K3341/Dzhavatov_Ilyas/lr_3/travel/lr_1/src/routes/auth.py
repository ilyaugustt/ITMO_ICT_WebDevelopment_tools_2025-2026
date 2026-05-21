"""Роуты для авторизации и аутентификации."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.schemas import (
    LoginRequest,
    TokenResponse,
)
from src.crud import UserCRUD
from src.models import User
from src.auth_utils import create_jwt, verify_password as verify_pw
from src.settings import Settings
from src.connection import get_db

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

settings = Settings()


def create_user_crud(db: Session = Depends(get_db)) -> UserCRUD:
    yield UserCRUD(db)


@auth_router.post(
    "/login",
    response_model=TokenResponse,
    summary="Авторизация",
)
def login(
    login_data: LoginRequest,
    user_crud: UserCRUD = Depends(create_user_crud),
):
    """
    Авторизация пользователя по username и password.
    Возвращает JWT токен.
    """
    print(f"Logging in user: {login_data.username}")
    user = user_crud.get_user_by_username(login_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Пользователь деактивирован",
        )
    if not verify_pw(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный пароль",
        )

    token = create_jwt(
        payload={"sub": str(user.id)},
        secret_key=settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
        expire_minutes=settings.jwt_expire_minutes,
    )

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        expires_in=settings.jwt_expire_minutes * 60,
    )
