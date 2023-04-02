from enum import Enum
from uuid import UUID
from datetime import datetime, timezone, timedelta
from typing import Final

class RegisterError(Enum):
    InvalidCredentials = 1
    UnexpectedError = 2

class DatabaseError(Enum):
    UnexpectedError = 1
    UserDoesNotExist = 2
    UserAlreadyExists = 3
    CompanyDoesNotExist = 4

class ServerConnectionError(Enum):
    UnexpectedError = 1

class TokenError(Enum):
    InvalidToken = 1
    MissingToken = 2

class TimeAuthorize:
    # 1 hour = 604_800 seconds
    EXPIREY_TIME_SECONDS: Final[int] = 604_800

    def current_time() -> datetime:
        return datetime.now(timezone.utc)

    def expirey_time(current_time: datetime) -> datetime:
        return current_time + timedelta(seconds = TimeAuthorize.EXPIREY_TIME_SECONDS)

    def create_expirey_time() -> datetime:
        return TimeAuthorize.current_time() + timedelta(seconds = TimeAuthorize.EXPIREY_TIME_SECONDS)

    def time_expired(time: datetime) -> bool:
        return TimeAuthorize.current_time() < time

    def time_to_timestamp(time: datetime) -> str:
        return str(datetime.timestamp(time))

    def timestamp_to_time(timestamp: float | str) -> str:
        return str(datetime.fromtimestamp(float(timestamp)))

class UserDetails:
    def __init__(self, username: str, email: str, id: UUID, exp: datetime):
        self.username = username
        self.email = email
        self.id = id
        self.exp = exp

    def to_dict(self) -> dict[str, str]:
        return {
            "username": self.username,
            "email": self.email,
            "id": str(self.id),
            "exp": TimeAuthorize.time_to_timestamp(self.exp)
        }

class StockRequest:
    def __init__(self, company: str, shares: int):
        self.company = company
        self.shares = shares
