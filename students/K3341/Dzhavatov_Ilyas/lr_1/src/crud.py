from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import Optional, List
from datetime import datetime
from .models import (
    User,
    Trip,
    TravelRequest,
    Destination,
    Message,
    Review,
)

from .schemas import UserBase, DestinationInDB, TripInDB


class UserCRUD:
    def __init__(self, db: Session):
        self._db = db

    def get_user_by_id(self, user_id: int) -> User | None:
        return self._db.query(User).filter(User.id == user_id).first()

    def get_user_by_username(self, username: str) -> Optional[User]:
        return self._db.query(User).filter(User.username == username).first()

    def get_users(
        self, skip: int = 0, limit: int = 100, active: bool = True
    ) -> list[UserBase]:
        query = self._db.query(User)
        if active:
            query = query.filter(User.is_active == True)

        users = query.offset(skip).limit(limit).all()

        return [UserBase.model_validate(user) for user in users]

    def create_user(
        self,
        username: str,
        email: str,
        hashed_password: str,
        full_name: Optional[str] = None,
        bio: Optional[str] = None,
        age: Optional[int] = None,
        gender: Optional[str] = None,
        skills: Optional[str] = None,
        experience: Optional[str] = None,
        preferences: Optional[str] = None,
        avatar_url: Optional[str] = None,
    ) -> User:
        user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            bio=bio,
            age=age,
            gender=gender,
            skills=skills,
            experience=experience,
            preferences=preferences,
            avatar_url=avatar_url,
        )
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)

        return user

    def update_user(self, user: User, **kwargs) -> User:
        for key, value in kwargs.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)
        self._db.commit()
        self._db.refresh(user)
        return user

    def deactivate_user(self, user: User) -> User:
        user.is_active = False
        self._db.commit()
        self._db.refresh(user)
        return user

    def add_preferred_destination(self, user: User, destination: Destination) -> User:
        if destination not in user.preferred_destinations:
            user.preferred_destinations.append(destination)
            self._db.commit()
            self._db.refresh(user)
        return user

    def remove_preferred_destination(
        self, user: User, destination: Destination
    ) -> User:
        if destination in user.preferred_destinations:
            user.preferred_destinations.remove(destination)
            self._db.commit()
            self._db.refresh(user)
        return user

    def delete_user(self, user: User) -> None:
        self._db.delete(user)
        self._db.commit()

    def verify_password(self, user: User, password: str) -> bool:
        """Проверяет пароль пользователя."""
        from src.auth_utils import verify_password as verify

        return verify(password, user.hashed_password)

    def change_password(self, user: User, new_password: str) -> User:
        """Меняет пароль пользователя."""
        from src.auth_utils import hash_password

        user.hashed_password = hash_password(new_password)
        self._db.commit()
        self._db.refresh(user)
        return user


def get_trip_by_id(db: Session, trip_id: int) -> Trip | None:
    """Получить поездку по ID с загруженными связями."""
    return (
        db.query(Trip)
        .options(
            joinedload(Trip.creator),
            joinedload(Trip.destinations),
            joinedload(Trip.travel_requests),
        )
        .filter(Trip.id == trip_id)
        .first()
    )


def get_trips(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: str | None = None,
    creator_id: int | None = None,
) -> list[Trip]:
    query = db.query(Trip)
    if status:
        query = query.filter(Trip.status == status)
    if creator_id:
        query = query.filter(Trip.creator_id == creator_id)

    trips = query.order_by(Trip.start_date).offset(skip).limit(limit).all()
    return [TripInDB.model_validate(trip) for trip in trips]


def get_active_trips_crud(db: Session, skip: int = 0, limit: int = 100) -> list[Trip]:
    return (
        db.query(Trip)
        .filter(Trip.status == "planned", Trip.end_date >= datetime.now().date())
        .order_by(Trip.start_date)
        .offset(skip)
        .limit(limit)
        .all()
    )


def search_trips(
    db: Session,
    start_location: Optional[str] = None,
    end_location: Optional[str] = None,
    start_date_from: Optional[datetime] = None,
    start_date_to: Optional[datetime] = None,
) -> list[Trip]:
    query = db.query(Trip)
    if start_location:
        query = query.filter(Trip.start_location.ilike(f"%{start_location}%"))
    if end_location:
        query = query.filter(Trip.end_location.ilike(f"%{end_location}%"))
    if start_date_from:
        query = query.filter(Trip.start_date >= start_date_from.date())
    if start_date_to:
        query = query.filter(Trip.start_date <= start_date_to.date())
    return query.all()


def create_trip(
    db: Session,
    title: str,
    description: str,
    start_location: str,
    end_location: str,
    start_date,
    end_date,
    creator_id: int,
    budget: Optional[float] = None,
    max_participants: int = 10,
    destinations: Optional[List[Destination]] = None,
    status: str = "planned",
) -> Trip:
    trip = Trip(
        title=title,
        description=description,
        start_location=start_location,
        end_location=end_location,
        start_date=start_date.date()
        if isinstance(start_date, datetime)
        else start_date,
        end_date=end_date.date() if isinstance(end_date, datetime) else end_date,
        creator_id=creator_id,
        budget=budget,
        max_participants=max_participants,
        status=status,
    )
    if destinations:
        trip.destinations.extend(destinations)
    db.add(trip)
    db.commit()
    db.refresh(trip)
    return trip


def update_trip(db: Session, trip: Trip, **kwargs) -> Trip:
    for key, value in kwargs.items():
        if hasattr(trip, key) and value is not None:
            setattr(trip, key, value)
    db.commit()
    db.refresh(trip)
    return trip


def update_trip_status(db: Session, trip: Trip, new_status: str) -> Trip:
    trip.status = new_status
    db.commit()
    db.refresh(trip)
    return trip


def add_destination_to_trip(db: Session, trip: Trip, destination: Destination) -> Trip:
    if destination not in trip.destinations:
        trip.destinations.append(destination)
        db.commit()
        db.refresh(trip)
    return trip


def remove_destination_from_trip(
    db: Session, trip: Trip, destination: Destination
) -> Trip:
    if destination in trip.destinations:
        trip.destinations.remove(destination)
        db.commit()
        db.refresh(trip)
    return trip


def delete_trip(db: Session, trip: Trip) -> None:
    db.delete(trip)
    db.commit()


def get_travel_request(
    db: Session, trip_id: int, user_id: int
) -> Optional[TravelRequest]:
    return (
        db.query(TravelRequest)
        .filter(TravelRequest.trip_id == trip_id, TravelRequest.user_id == user_id)
        .first()
    )


def get_travel_requests_for_trip(
    db: Session, trip_id: int, status: Optional[str] = None
) -> List[TravelRequest]:
    query = db.query(TravelRequest).filter(TravelRequest.trip_id == trip_id)
    if status:
        query = query.filter(TravelRequest.status == status)
    return query.all()


def get_travel_requests_for_user(
    db: Session, user_id: int, status: Optional[str] = None
) -> List[TravelRequest]:
    query = db.query(TravelRequest).filter(TravelRequest.user_id == user_id)
    if status:
        query = query.filter(TravelRequest.status == status)
    return query.all()


def create_travel_request(
    db: Session, trip_id: int, user_id: int, message: Optional[str] = None
) -> TravelRequest:
    existing_request = get_travel_request(db, trip_id, user_id)
    if existing_request:
        return existing_request
    request = TravelRequest(
        trip_id=trip_id, user_id=user_id, message=message, status="pending"
    )
    db.add(request)
    db.commit()
    db.refresh(request)
    return request


def update_travel_request_status(
    db: Session, request: TravelRequest, new_status: str
) -> TravelRequest:
    request.status = new_status
    db.commit()
    db.refresh(request)
    return request


def delete_travel_request(db: Session, request: TravelRequest) -> None:
    db.delete(request)
    db.commit()


def get_destination_by_id(db: Session, destination_id: int) -> Optional[Destination]:
    return (
        db.query(Destination)
        .options(
            joinedload(Destination.interested_users), joinedload(Destination.trips)
        )
        .filter(Destination.id == destination_id)
        .first()
    )


def get_destination_by_name(db: Session, name: str) -> Destination | None:
    return db.query(Destination).filter(Destination.name == name).first()


def get_destinations(
    db: Session, skip: int = 0, limit: int = 100, country: Optional[str] = None
) -> list[DestinationInDB]:
    query = db.query(Destination)
    if country:
        query = query.filter(Destination.country.ilike(f"%{country}%"))
    destinations = (
        query.order_by(Destination.popularity.desc()).offset(skip).limit(limit).all()
    )

    return [DestinationInDB.model_validate(destination) for destination in destinations]


def search_destinations(db: Session, query_text: str) -> List[Destination]:
    search_pattern = f"%{query_text}%"
    return (
        db.query(Destination)
        .filter(
            Destination.name.ilike(search_pattern)
            | Destination.description.ilike(search_pattern)
        )
        .all()
    )


def create_destination(
    db: Session,
    name: str,
    country: str,
    description: Optional[str] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
) -> Destination:
    destination = Destination(
        name=name,
        country=country,
        description=description,
        latitude=latitude,
        longitude=longitude,
    )
    db.add(destination)
    db.commit()
    db.refresh(destination)
    return destination


def update_destination(db: Session, destination: Destination, **kwargs) -> Destination:
    for key, value in kwargs.items():
        if hasattr(destination, key) and value is not None:
            setattr(destination, key, value)
    db.commit()
    db.refresh(destination)
    return destination


def update_popularity(
    db: Session, destination: Destination, increment: bool = True
) -> Destination:
    if increment:
        destination.popularity += 1
    else:
        destination.popularity = max(0, destination.popularity - 1)
    db.commit()
    db.refresh(destination)
    return destination


def delete_destination(db: Session, destination: Destination) -> None:
    db.delete(destination)
    db.commit()


def get_message_by_id(db: Session, message_id: int) -> Optional[Message]:
    return (
        db.query(Message)
        .options(joinedload(Message.sender), joinedload(Message.receiver))
        .filter(Message.id == message_id)
        .first()
    )


def get_messages_for_trip(
    db: Session, trip_id: int, skip: int = 0, limit: int = 50
) -> List[Message]:
    return (
        db.query(Message)
        .filter(Message.trip_id == trip_id)
        .order_by(Message.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_messages_between_users(
    db: Session,
    user1_id: int,
    user2_id: int,
    trip_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 50,
) -> List[Message]:
    query = db.query(Message).filter(
        ((Message.sender_id == user1_id) & (Message.receiver_id == user2_id))
        | ((Message.sender_id == user2_id) & (Message.receiver_id == user1_id))
    )
    if trip_id:
        query = query.filter(Message.trip_id == trip_id)
    return query.order_by(Message.created_at.desc()).offset(skip).limit(limit).all()


def create_message(
    db: Session, content: str, trip_id: int, sender_id: int, receiver_id: int
) -> Message:
    message = Message(
        content=content, trip_id=trip_id, sender_id=sender_id, receiver_id=receiver_id
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def delete_message(db: Session, message: Message) -> None:
    db.delete(message)
    db.commit()


def get_review_by_id(db: Session, review_id: int) -> Optional[Review]:
    return (
        db.query(Review)
        .options(
            joinedload(Review.reviewer),
            joinedload(Review.reviewed_user),
            joinedload(Review.trip),
        )
        .filter(Review.id == review_id)
        .first()
    )


def get_reviews_for_user(
    db: Session, user_id: int, skip: int = 0, limit: int = 100
) -> List[Review]:
    return (
        db.query(Review)
        .filter(Review.reviewed_user_id == user_id)
        .order_by(Review.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_reviews_by_reviewer(
    db: Session, reviewer_id: int, skip: int = 0, limit: int = 100
) -> List[Review]:
    return (
        db.query(Review)
        .filter(Review.reviewer_id == reviewer_id)
        .order_by(Review.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_review_for_trip(
    db: Session, trip_id: int, reviewer_id: int, reviewed_user_id: int
) -> Optional[Review]:
    return (
        db.query(Review)
        .filter(
            Review.trip_id == trip_id,
            Review.reviewer_id == reviewer_id,
            Review.reviewed_user_id == reviewed_user_id,
        )
        .first()
    )


def calculate_user_rating(db: Session, user_id: int) -> Optional[float]:
    result = (
        db.query(func.avg(Review.rating))
        .filter(Review.reviewed_user_id == user_id)
        .scalar()
    )
    return round(result, 2) if result else None


def create_review(
    db: Session,
    comment: Optional[str],
    rating: int,
    trip_id: int,
    reviewer_id: int,
    reviewed_user_id: int,
) -> Review:
    existing_review = get_review_for_trip(db, trip_id, reviewer_id, reviewed_user_id)
    if existing_review:
        return existing_review
    review = Review(
        comment=comment,
        rating=rating,
        trip_id=trip_id,
        reviewer_id=reviewer_id,
        reviewed_user_id=reviewed_user_id,
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


def update_review(db: Session, review: Review, **kwargs) -> Review:
    for key, value in kwargs.items():
        if hasattr(review, key) and value is not None:
            setattr(review, key, value)
    db.commit()
    db.refresh(review)
    return review


def delete_review(db: Session, review: Review) -> None:
    db.delete(review)
    db.commit()
