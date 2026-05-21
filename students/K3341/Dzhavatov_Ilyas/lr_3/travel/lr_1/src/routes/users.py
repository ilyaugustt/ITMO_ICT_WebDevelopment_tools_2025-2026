"""Роуты для управления пользователями."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.schemas import (
    UserCreate,
    UserUpdate,
    UserInDB,
    UserBase,
    UserWithDestinations,
)
from src.crud import UserCRUD
from src.models import User
from src.auth_utils import hash_password
from src.connection import get_db

user_router = APIRouter(prefix="/users", tags=["Users"])


def create_user_crud(db: Session = Depends(get_db)) -> UserCRUD:
    yield UserCRUD(db)


@user_router.post(
    "/",
    response_model=UserInDB,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user_data: UserCreate,
    user_crud: UserCRUD = Depends(create_user_crud),
):
    existing_user = user_crud.get_user_by_username(user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username уже занят"
        )
    existing_email = user_crud._db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email уже занят"
        )
    hashed = hash_password(user_data.password)
    return user_crud.create_user(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed,
        full_name=user_data.full_name,
        bio=user_data.bio,
        age=user_data.age,
        gender=user_data.gender,
        skills=user_data.skills,
        experience=user_data.experience,
        preferences=user_data.preferences,
        avatar_url=user_data.avatar_url,
    )


@user_router.get("/", response_model=list[UserBase])
def get_users(
    active: bool = True,
    user_crud: UserCRUD = Depends(create_user_crud),
):
    users = user_crud.get_users(active=active)
    return users


@user_router.get("/{user_id}", response_model=UserWithDestinations)
def get_user(
    user_id: int,
    user_crud: UserCRUD = Depends(create_user_crud),
):
    user = user_crud.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
        )
    return user


@user_router.patch("/{user_id}", response_model=UserInDB)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    user_crud: UserCRUD = Depends(create_user_crud),
):
    user = user_crud.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
        )
    return user_crud.update_user(user, **user_update.model_dump(exclude_unset=True))


@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    user_crud: UserCRUD = Depends(create_user_crud),
):
    user = user_crud.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
        )
    user_crud.delete_user(user)
