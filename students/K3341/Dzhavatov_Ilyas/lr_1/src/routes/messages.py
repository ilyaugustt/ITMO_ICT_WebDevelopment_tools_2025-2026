"""Роуты для управления сообщениями."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from src.schemas import (
    MessageCreate,
    MessageInDB,
    MessageWithUsers,
    PaginationParams,
)
from src.crud import (
    get_messages_for_trip,
    get_messages_between_users,
    create_message,
    get_trip_by_id,
)
from src.crud import UserCRUD
from src.connection import get_db

message_router = APIRouter(prefix="/messages", tags=["Messages"])


def create_user_crud(db: Session = Depends(get_db)) -> UserCRUD:
    yield UserCRUD(db)


@message_router.post(
    "/",
    response_model=MessageInDB,
    status_code=status.HTTP_201_CREATED,
    summary="Создать сообщение",
)
def create_message_endpoint(
    message_data: MessageCreate,
    db: Session = Depends(get_db),
    user_crud: UserCRUD = Depends(create_user_crud),
):
    trip = get_trip_by_id(db, message_data.trip_id)
    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Поездка не найдена"
        )
    sender = user_crud.get_user_by_id(db, message_data.sender_id)
    receiver = user_crud.get_user_by_id(db, message_data.receiver_id)
    if not sender or not receiver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
        )
    return create_message(db, **message_data.model_dump())


@message_router.get(
    "/trip/{trip_id}",
    response_model=list[MessageWithUsers],
)
def get_messages_for_trip_endpoint(
    trip_id: int,
    pagination: PaginationParams = Query(...),
    db: Session = Depends(get_db),
):
    return get_messages_for_trip(
        db, trip_id, skip=pagination.skip, limit=pagination.limit
    )


@message_router.get(
    "/between",
    response_model=list[MessageWithUsers],
)
def get_messages_between_users_endpoint(
    user1_id: int,
    user2_id: int,
    trip_id: int | None = None,
    pagination: PaginationParams = Query(...),
    db: Session = Depends(get_db),
):
    return get_messages_between_users(
        db,
        user1_id,
        user2_id,
        trip_id=trip_id,
        skip=pagination.skip,
        limit=pagination.limit,
    )
