from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    DateTime,
    Boolean,
    Enum,
    ForeignKey,
    Table,
    Text,
    CheckConstraint,
    Index,
)
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from datetime import datetime, date
from typing import Optional
import enum


# =============================================================================
# Базовый класс для SQLAlchemy моделей
# =============================================================================


class Base(DeclarativeBase):
    pass


# =============================================================================
# Enum для типов данных
# =============================================================================


class TripStatus(str, enum.Enum):
    """Статус поездки."""

    PLANNED = "planned"  # Планируется
    ONGOING = "ongoing"  # В процессе
    COMPLETED = "completed"  # Завершена
    CANCELLED = "cancelled"  # Отменена


class TravelRequestStatus(str, enum.Enum):
    """Статус запроса на участие."""

    PENDING = "pending"  # Ожидает ответа
    ACCEPTED = "accepted"  # Принят
    REJECTED = "rejected"  # Отклонён


class Gender(str, enum.Enum):
    """Пол пользователя."""

    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


# =============================================================================
# Ассоциативные таблицы для Many-to-Many связей
# =============================================================================

# Many-to-Many: User <-> Destination (предпочтения пользователей)
# Ассоциативная сущность с полем preference_level
user_destinations = Table(
    "user_destinations",
    Base.metadata,
    Column(
        "user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    ),
    Column(
        "destination_id",
        Integer,
        ForeignKey("destinations.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

# Many-to-Many: Trip <-> Destination (маршрут поездки)
# Ассоциативная сущность с полем order_number
trip_destinations = Table(
    "trip_destinations",
    Base.metadata,
    Column(
        "trip_id", Integer, ForeignKey("trips.id", ondelete="CASCADE"), primary_key=True
    ),
    Column(
        "destination_id",
        Integer,
        ForeignKey("destinations.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


# =============================================================================
# Таблица 1: Users (Пользователи / Профили)
# =============================================================================


class User(Base):
    """Модель профиля пользователя."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    email: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(100))
    bio: Mapped[Optional[str]] = mapped_column(Text)  # О себе
    age: Mapped[Optional[int]] = mapped_column(Integer)
    gender: Mapped[Optional[Gender]] = mapped_column(Enum(Gender))
    skills: Mapped[Optional[str]] = mapped_column(
        Text
    )  # Навыки (например: вождение, фотография, готовка)
    experience: Mapped[Optional[str]] = mapped_column(Text)  # Опыт путешествий
    preferences: Mapped[Optional[str]] = mapped_column(
        Text
    )  # Предпочтения по проектам/поездкам
    avatar_url: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )

    # Relationships (One-to-Many)
    created_trips: Mapped[list["Trip"]] = relationship(
        back_populates="creator", cascade="all, delete-orphan"
    )
    travel_requests: Mapped[list["TravelRequest"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    # Many-to-Many через ассоциативную таблицу (предпочтения направлений)
    preferred_destinations: Mapped[list["Destination"]] = relationship(
        secondary=user_destinations, back_populates="interested_users"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"


# =============================================================================
# Таблица 2: Trips (Поездки)
# =============================================================================


class Trip(Base):
    """Модель поездки."""

    __tablename__ = "trips"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    start_location: Mapped[str] = mapped_column(
        String(100), nullable=False
    )  # Место отправления
    end_location: Mapped[str] = mapped_column(
        String(100), nullable=False
    )  # Место назначения
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[TripStatus] = mapped_column(
        Enum(TripStatus), default=TripStatus.PLANNED
    )
    budget: Mapped[Optional[float]] = mapped_column(Float)  # Бюджет поездки
    max_participants: Mapped[int] = mapped_column(Integer, default=10)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )

    # Foreign Key (One-to-Many связь)
    creator_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # Relationships
    creator: Mapped["User"] = relationship(back_populates="created_trips")

    # Many-to-Many через ассоциативную таблицу (маршрут)
    destinations: Mapped[list["Destination"]] = relationship(
        secondary=trip_destinations, back_populates="trips"
    )

    # One-to-Many: запросы на участие
    travel_requests: Mapped[list["TravelRequest"]] = relationship(
        back_populates="trip", cascade="all, delete-orphan"
    )

    # Ограничения
    __table_args__ = (
        CheckConstraint("end_date >= start_date", name="ck_trips_dates_valid"),
        CheckConstraint("budget >= 0", name="ck_trips_budget_non_negative"),
        CheckConstraint(
            "max_participants > 0", name="ck_trips_max_participants_positive"
        ),
        Index("ix_trips_dates", "start_date", "end_date"),
        Index("ix_trips_locations", "start_location", "end_location"),
    )

    def __repr__(self) -> str:
        return f"<Trip(id={self.id}, title='{self.title}', status={self.status})>"


# =============================================================================
# Таблица 3: TravelRequests (Запросы на участие) — Ассоциативная сущность
# =============================================================================


class TravelRequest(Base):
    """
    Ассоциативная сущность для связи Many-to-Many между Trip и User.
    Представляет запрос пользователя на участие в поездке.
    Имеет поле status для характеризации связи.
    """

    __tablename__ = "travel_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    message: Mapped[Optional[str]] = mapped_column(Text)  # Сообщение от пользователя
    status: Mapped[TravelRequestStatus] = mapped_column(
        Enum(TravelRequestStatus), default=TravelRequestStatus.PENDING, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )

    # Foreign Keys
    trip_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("trips.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # Relationships
    trip: Mapped["Trip"] = relationship(back_populates="travel_requests")
    user: Mapped["User"] = relationship(back_populates="travel_requests")

    # Уникальное ограничение: один пользователь — один запрос на одну поездку
    __table_args__ = (
        # Один пользователь не может отправить несколько запросов на одну поездку
        # (можно удалить и создать новый с другим статусом)
        Index("ix_travel_requests_trip_user", "trip_id", "user_id", unique=True),
    )

    def __repr__(self) -> str:
        return f"<TravelRequest(id={self.id}, trip_id={self.trip_id}, user_id={self.user_id}, status={self.status})>"


# =============================================================================
# Таблица 4: Destinations (Направления / Места)
# =============================================================================


class Destination(Base):
    """Модель направления/места посещения."""

    __tablename__ = "destinations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True
    )
    country: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    latitude: Mapped[Optional[float]] = mapped_column(Float)
    longitude: Mapped[Optional[float]] = mapped_column(Float)
    popularity: Mapped[int] = mapped_column(
        Integer, default=0
    )  # Количество интересующихся

    # Relationships (Many-to-Many)
    # Пользователи, которые заинтересованы в этом направлении
    interested_users: Mapped[list["User"]] = relationship(
        secondary=user_destinations, back_populates="preferred_destinations"
    )
    # Поездки, которые посещают это направление
    trips: Mapped[list["Trip"]] = relationship(
        secondary=trip_destinations, back_populates="destinations"
    )

    def __repr__(self) -> str:
        return (
            f"<Destination(id={self.id}, name='{self.name}', country='{self.country}')>"
        )


# =============================================================================
# Таблица 5: Messages (Сообщения между участниками)
# =============================================================================


class Message(Base):
    """Модель сообщения между участниками поездки."""

    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    # Foreign Keys
    trip_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("trips.id", ondelete="CASCADE"), nullable=False, index=True
    )
    sender_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    receiver_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # Relationships
    trip: Mapped["Trip"] = relationship()
    sender: Mapped["User"] = relationship(foreign_keys=[sender_id])
    receiver: Mapped["User"] = relationship(foreign_keys=[receiver_id])

    __table_args__ = (Index("ix_messages_trip_created", "trip_id", "created_at"),)

    def __repr__(self) -> str:
        return f"<Message(id={self.id}, trip_id={self.trip_id}, from={self.sender_id}, to={self.receiver_id})>"


# =============================================================================
# Таблица 6: Reviews (Отзывы о пользователях)
# =============================================================================


class Review(Base):
    """Модель отзыва о пользователе."""

    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    comment: Mapped[Optional[str]] = mapped_column(Text)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    # Foreign Keys
    reviewer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    reviewed_user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    trip_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("trips.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # Relationships
    reviewer: Mapped["User"] = relationship(foreign_keys=[reviewer_id])
    reviewed_user: Mapped["User"] = relationship(foreign_keys=[reviewed_user_id])
    trip: Mapped["Trip"] = relationship()

    # Ограничения
    __table_args__ = (
        CheckConstraint("rating >= 1 AND rating <= 5", name="ck_reviews_rating_valid"),
        Index("ix_reviews_trip_reviewer", "trip_id", "reviewer_id", unique=True),
    )

    def __repr__(self) -> str:
        return f"<Review(id={self.id}, rating={self.rating}, from={self.reviewer_id})>"
