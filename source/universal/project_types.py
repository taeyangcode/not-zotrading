from enum import Enum
from uuid import UUID

class RegisterError(Enum):
    InvalidCredentials = 1
    UnexpectedError = 2

class DatabaseError(Enum):
    UnexpectedError = 1
    UserDoesNotExist = 2

class ServerConnectionError(Enum):
    UnexpectedError = 1

class UserDetails:
    def __init__(self, username: str, email: str, id: UUID):
        self.username = username
        self.email = email
        self.id = id

class StockRequest:
    def __init__(self, company: str, shares: int):
        self.company = company
        self.shares = shares
