from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime, date
from enum import Enum
from pydantic_settings import SettingsConfigDict


class TripStatusEnum(str, Enum):
    PLANNED = "planned"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TravelRequestStatusEnum(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class GenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore")
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(..., max_length=100)
    full_name: str | None = Field(None, max_length=100)
    bio: str | None = None
    age: int | None = None
    gender: GenderEnum | None = None
    skills: str | None = None
    experience: str | None = None
    preferences: str | None = None
    avatar_url: str | None = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=255)


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, max_length=100)
    bio: str | None = None
    age: int | None = None
    gender: GenderEnum | None = None
    skills: str | None = None
    experience: str | None = None
    preferences: str | None = None
    avatar_url: str | None = None


class UserInDB(UserBase):
    id: int
    is_active: bool = True
    created_at: datetime
    updated_at: datetime | None = None

    model_config = SettingsConfigDict(from_attributes=True)


class UserWithDestinations(UserInDB):
    preferred_destinations: Optional[List["DestinationInDB"]] = None


class TripBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(...)
    start_location: str = Field(..., max_length=100)
    end_location: str = Field(..., max_length=100)
    start_date: date
    end_date: date
    budget: float | None = Field(None, ge=0)
    max_participants: int = Field(..., ge=1, le=1000)
    status: TripStatusEnum = TripStatusEnum.PLANNED


class TripCreate(TripBase):
    creator_id: int


class TripUpdate(BaseModel):
    title: str | None = Field(None, max_length=100)
    description: str | None = None
    start_location: str | None = Field(None, max_length=100)
    end_location: str | None = Field(None, max_length=100)
    start_date: date | None = None
    end_date: date | None = None
    budget: float | None = Field(None, ge=0)
    max_participants: int | None = Field(None, ge=1)
    status: TripStatusEnum | None = None


class TripInDB(TripBase):
    id: int
    creator_id: int
    created_at: datetime
    updated_at: datetime | None = None

    model_config = SettingsConfigDict(from_attributes=True)


class DestinationBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    country: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class DestinationInDB(DestinationBase):
    id: int
    popularity: int = 0

    model_config = SettingsConfigDict(from_attributes=True)


class TravelRequestBase(BaseModel):
    message: Optional[str] = None
    status: TravelRequestStatusEnum = TravelRequestStatusEnum.PENDING


class TravelRequestInDB(TravelRequestBase):
    """Схема запроса с ID и временными метками."""

    id: int
    trip_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}


class TripWithDetails(TripInDB):
    creator: UserInDB | None = None
    destinations: list[DestinationInDB] | None = None
    travel_requests: list[TravelRequestInDB] | None = None


class TravelRequestCreate(TravelRequestBase):
    trip_id: int
    user_id: int


class TravelRequestUpdate(BaseModel):
    status: TravelRequestStatusEnum


class TravelRequestWithUser(TravelRequestInDB):
    user: UserInDB | None = None


class DestinationCreate(DestinationBase):
    pass


class DestinationUpdate(BaseModel):
    name: str | None = Field(None, max_length=100)
    country: str | None = Field(None, max_length=50)
    description: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    popularity: int | None = None


class DestinationWithDetails(DestinationInDB):
    interested_users: list[UserInDB] | None = None
    trips: list[TripInDB] | None = None


class MessageBase(BaseModel):
    content: str = Field(..., min_length=1)


class MessageCreate(MessageBase):
    trip_id: int
    sender_id: int
    receiver_id: int


class MessageInDB(MessageBase):
    id: int
    trip_id: int
    sender_id: int
    receiver_id: int
    created_at: datetime

    model_config = SettingsConfigDict(from_attributes=True)


class MessageWithUsers(MessageInDB):
    sender: UserInDB | None = None
    receiver: UserInDB | None = None


class ReviewBase(BaseModel):
    """Базовая схема отзыва."""

    comment: str | None = None
    rating: int = Field(..., ge=1, le=5)


class ReviewCreate(ReviewBase):
    trip_id: int
    reviewer_id: int
    reviewed_user_id: int


class ReviewUpdate(BaseModel):
    comment: str | None = None
    rating: int | None = Field(None, ge=1, le=5)


class ReviewInDB(ReviewBase):
    id: int
    trip_id: int
    reviewer_id: int
    reviewed_user_id: int
    created_at: datetime

    model_config = SettingsConfigDict(from_attributes=True)


class ReviewWithUsers(ReviewInDB):
    reviewer: UserInDB | None = None
    reviewed_user: UserInDB | None = None


class PaginationParams(BaseModel):
    skip: int = Field(0, ge=0)
    limit: int = Field(100, ge=1, le=1000)


class ResponseList(BaseModel):
    total: int
    skip: int
    limit: int
    items: List


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=1, max_length=255)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class PasswordUpdate(BaseModel):
    old_password: str = Field(..., min_length=1, max_length=255)
    new_password: str = Field(..., min_length=8, max_length=255)
