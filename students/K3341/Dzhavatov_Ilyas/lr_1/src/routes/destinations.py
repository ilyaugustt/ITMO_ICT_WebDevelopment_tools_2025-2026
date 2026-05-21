"""Роуты для управления направлениями."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.schemas import (
    DestinationCreate,
    DestinationUpdate,
    DestinationInDB,
    DestinationWithDetails,
)
from src.crud import (
    get_destination_by_id,
    get_destination_by_name,
    get_destinations,
    search_destinations,
    create_destination,
    update_destination,
    update_popularity,
    delete_destination,
)

from src.connection import get_db

destination_router = APIRouter(prefix="/destinations", tags=["Destinations"])


@destination_router.post(
    "/",
    response_model=DestinationInDB,
    status_code=status.HTTP_201_CREATED,
)
def create_destination_endpoint(
    destination_data: DestinationCreate,
    db: Session = Depends(get_db),
):
    existing = get_destination_by_name(db, destination_data.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Направление с таким названием уже существует",
        )
    return create_destination(db, **destination_data.model_dump())


@destination_router.get("/", response_model=list[DestinationInDB])
def get_destinations_endpoint(
    country: str | None = None,
    db: Session = Depends(get_db),
):
    destinations = get_destinations(db, country=country)
    return destinations


@destination_router.get("/search", response_model=list[DestinationInDB])
def search_destinations_endpoint(
    query: str,
    db: Session = Depends(get_db),
):
    return search_destinations(db, query_text=query)


@destination_router.get(
    "/{destination_id}",
    response_model=DestinationWithDetails,
)
def get_destination(
    destination_id: int,
    db: Session = Depends(get_db),
):
    """Получить направление по ID."""
    destination = get_destination_by_id(db, destination_id)
    if not destination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Направление не найдено"
        )
    return destination


@destination_router.patch("/{destination_id}", response_model=DestinationInDB)
def update_destination_(
    destination_id: int,
    destination_update: DestinationUpdate,
    db: Session = Depends(get_db),
):
    destination = get_destination_by_id(db, destination_id)
    if not destination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Направление не найдено"
        )
    return update_destination(
        db, destination, **destination_update.model_dump(exclude_unset=True)
    )


@destination_router.post(
    "/{destination_id}/popularity",
    response_model=DestinationInDB,
)
def update_destination_popularity(
    destination_id: int,
    increment: bool = True,
    db: Session = Depends(get_db),
):
    destination = get_destination_by_id(db, destination_id)
    if not destination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Направление не найдено"
        )
    return update_popularity(db, destination, increment=increment)


@destination_router.delete(
    "/{destination_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_destination(
    destination_id: int,
    db: Session = Depends(get_db),
):
    destination = get_destination_by_id(db, destination_id)
    if not destination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Направление не найдено"
        )
    delete_destination(db, destination)
