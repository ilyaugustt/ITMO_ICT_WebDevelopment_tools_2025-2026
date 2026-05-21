"""Роуты для управления запросами на участие в поездках."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.schemas import (
    TravelRequestCreate,
    TravelRequestUpdate,
    TravelRequestInDB,
    TravelRequestWithUser,
    TravelRequestStatusEnum,
)
from src.crud import (
    get_travel_requests_for_trip,
    get_travel_requests_for_user,
    create_travel_request,
    get_trip_by_id,
)
from src.crud import UserCRUD
from src.connection import get_db

travel_request_router = APIRouter(prefix="/travel-requests", tags=["Travel Requests"])


def create_user_crud(db: Session = Depends(get_db)) -> UserCRUD:
    yield UserCRUD(db)


@travel_request_router.post(
    "/",
    response_model=TravelRequestInDB,
    status_code=status.HTTP_201_CREATED,
)
def create_travel_request_endpoint(
    request_data: TravelRequestCreate,
    db: Session = Depends(get_db),
    user_crud: UserCRUD = Depends(create_user_crud),
):
    """Создать запрос на участие в поездке."""
    user = user_crud.get_user_by_id(db, request_data.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
        )
    trip = get_trip_by_id(db, request_data.trip_id)
    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Поездка не найдена"
        )
    return create_travel_request(db, **request_data.model_dump())


@travel_request_router.get(
    "/trip/{trip_id}",
    response_model=list[TravelRequestWithUser],
    summary="Получить запросы для поездки",
)
def get_travel_requests_for_trip_endpoint(
    trip_id: int,
    status_filter: TravelRequestStatusEnum | None = None,
    db: Session = Depends(get_db),
):
    """Получить все запросы для конкретной поездки."""
    return get_travel_requests_for_trip(
        db, trip_id, status=status_filter.value if status_filter else None
    )


@travel_request_router.get(
    "/user/{user_id}",
    response_model=list[TravelRequestInDB],
    summary="Получить запросы пользователя",
)
def get_travel_requests_for_user_endpoint(
    user_id: int,
    status_filter: TravelRequestStatusEnum | None = None,
    db: Session = Depends(get_db),
):
    """Получить все запросы пользователя."""
    return get_travel_requests_for_user(
        db, user_id, status=status_filter.value if status_filter else None
    )


@travel_request_router.patch(
    "/{request_id}", response_model=TravelRequestInDB, summary="Обновить статус запроса"
)
def update_travel_request(
    request_id: int,
    request_update: TravelRequestUpdate,
    db: Session = Depends(get_db),
):
    """Обновить статус запроса на участие."""
    # TODO: Добавить получение запроса по ID
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)
