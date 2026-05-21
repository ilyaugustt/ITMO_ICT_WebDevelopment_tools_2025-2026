"""Роуты для управления поездками."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.schemas import (
    TripCreate,
    TripUpdate,
    TripInDB,
    TripWithDetails,
    TripStatusEnum,
)
from src.crud import (
    get_trip_by_id,
    get_trips as crud_get_trips,
    get_active_trips_crud,
    search_trips,
    create_trip,
    update_trip,
    add_destination_to_trip as crud_add_destination_to_trip,
    remove_destination_from_trip as crud_remove_destination_from_trip,
    delete_trip,
    get_destination_by_id,
)
from src.crud import UserCRUD
from src.connection import get_db

trip_router = APIRouter(prefix="/trips", tags=["Trips"])


def create_user_crud(db: Session = Depends(get_db)) -> UserCRUD:
    yield UserCRUD(db)


@trip_router.post(
    "/",
    response_model=TripInDB,
    status_code=status.HTTP_201_CREATED,
    summary="Создать поездку",
)
def create_trip(
    trip_data: TripCreate,
    db: Session = Depends(get_db),
    user_crud: UserCRUD = Depends(create_user_crud),
):
    creator = user_crud.get_user_by_id(trip_data.creator_id)
    if not creator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Создатель не найден"
        )
    return create_trip(db, **trip_data.model_dump())


@trip_router.get("/", response_model=list[TripInDB])
def get_trips(
    status_filter: TripStatusEnum | None = None,
    creator_id: int | None = None,
    db: Session = Depends(get_db),
):
    trips = crud_get_trips(
        db,
        status=status_filter.value if status_filter else None,
        creator_id=creator_id,
    )
    return trips


@trip_router.get("/active", response_model=list[TripInDB])
def get_active_trips(db: Session = Depends(get_db)):
    """Получить активные (запланированные) поездки."""
    return get_active_trips_crud(db)


@trip_router.get("/search", response_model=list[TripInDB], summary="Поиск поездок")
def search_trips_endpoint(
    start_location: str | None = None,
    end_location: str | None = None,
    db: Session = Depends(get_db),
):
    """Поиск поездок по местам."""
    return search_trips(db, start_location=start_location, end_location=end_location)


@trip_router.get(
    "/{trip_id}", response_model=TripWithDetails, summary="Получить поездку"
)
def get_trip(trip_id: int, db: Session = Depends(get_db)):
    """Получить поездку по ID."""
    trip = get_trip_by_id(db, trip_id)
    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Поездка не найдена"
        )
    return trip


@trip_router.patch("/{trip_id}", response_model=TripInDB, summary="Обновить поездку")
def update_trip_endpoint(
    trip_id: int,
    trip_update: TripUpdate,
    db: Session = Depends(get_db),
):
    """Обновить данные поездки."""
    trip = get_trip_by_id(db, trip_id)
    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Поездка не найдена"
        )
    return update_trip(db, trip, **trip_update.model_dump(exclude_unset=True))


@trip_router.post(
    "/{trip_id}/destinations/{destination_id}",
    response_model=TripInDB,
    summary="Добавить направление в поездку",
)
def add_destination_to_trip(
    trip_id: int,
    destination_id: int,
    db: Session = Depends(get_db),
):
    """Добавить направление к маршруту поездки."""
    trip = get_trip_by_id(db, trip_id)
    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Поездка не найдена"
        )
    destination = get_destination_by_id(db, destination_id)
    if not destination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Направление не найдено"
        )
    return crud_add_destination_to_trip(db, trip, destination)


@trip_router.delete(
    "/{trip_id}/destinations/{destination_id}",
    response_model=TripInDB,
    summary="Удалить направление из поездки",
)
def remove_destination_from_trip(
    trip_id: int,
    destination_id: int,
    db: Session = Depends(get_db),
):
    """Удалить направление из маршрута поездки."""
    trip = get_trip_by_id(db, trip_id)
    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Поездка не найдена"
        )
    destination = get_destination_by_id(db, destination_id)
    if not destination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Направление не найдено"
        )
    return crud_remove_destination_from_trip(db, trip, destination)


@trip_router.delete(
    "/{trip_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить поездку"
)
def delete_trip(trip_id: int, db: Session = Depends(get_db)):
    """Удалить поездку."""
    trip = get_trip_by_id(db, trip_id)
    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Поездка не найдена"
        )
    delete_trip(db, trip)
