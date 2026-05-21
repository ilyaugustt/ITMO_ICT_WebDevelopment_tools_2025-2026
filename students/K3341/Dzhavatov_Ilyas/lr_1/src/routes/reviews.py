"""Роуты для управления отзывами."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from src.schemas import (
    ReviewCreate,
    ReviewInDB,
    PaginationParams,
    ResponseList,
)
from src.crud import (
    get_reviews_for_user,
    calculate_user_rating,
    create_review,
    get_trip_by_id,
)
from src.crud import UserCRUD
from src.connection import get_db

review_router = APIRouter(prefix="/reviews", tags=["Reviews"])


def create_user_crud(db: Session = Depends(get_db)) -> UserCRUD:
    yield UserCRUD(db)


@review_router.post(
    "/",
    response_model=ReviewInDB,
    status_code=status.HTTP_201_CREATED,
)
def create_review_endpoint(
    review_data: ReviewCreate,
    db: Session = Depends(get_db),
    user_crud: UserCRUD = Depends(create_user_crud),
):
    trip = get_trip_by_id(db, review_data.trip_id)
    reviewer = user_crud.get_user_by_id(db, review_data.reviewer_id)
    reviewed_user = user_crud.get_user_by_id(db, review_data.reviewed_user_id)
    if not trip or not reviewer or not reviewed_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь или поездка не найдены",
        )
    return create_review(db, **review_data.model_dump())


@review_router.get(
    "/user/{user_id}",
    response_model=ResponseList,
)
def get_reviews_for_user_endpoint(
    user_id: int,
    pagination: PaginationParams = Query(...),
    db: Session = Depends(get_db),
):
    reviews = get_reviews_for_user(
        db, user_id, skip=pagination.skip, limit=pagination.limit
    )
    return ResponseList(
        total=len(reviews), skip=pagination.skip, limit=pagination.limit, items=reviews
    )


@review_router.get("/user/{user_id}/rating")
def get_user_rating(
    user_id: int,
    db: Session = Depends(get_db),
):
    rating = calculate_user_rating(db, user_id)
    if rating is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="У пользователя нет отзывов"
        )
    return {
        "user_id": user_id,
        "average_rating": rating,
        "total_reviews": len(get_reviews_for_user(db, user_id)),
    }


@review_router.delete(
    "/{review_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить отзыв"
)
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
):
    # TODO: Добавить получение отзыва по ID
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)
