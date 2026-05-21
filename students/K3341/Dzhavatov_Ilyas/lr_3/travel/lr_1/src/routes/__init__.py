from .auth import auth_router
from .users import user_router
from .trips import trip_router
from .travel_requests import travel_request_router
from .destinations import destination_router
from .messages import message_router
from .reviews import review_router

__all__ = [
    "auth_router",
    "user_router",
    "trip_router",
    "travel_request_router",
    "destination_router",
    "message_router",
    "review_router",
]
