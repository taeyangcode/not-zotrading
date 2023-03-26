from enum import Enum
import uuid

class RegisterError(Enum):
    InvalidCredentials = 1
    UnexpectedError = 2

class ClientEvents(Enum):
    Register = "register"
    Login = "login"

class DatabaseCreate(Enum):
    CreateSuccess = 1
    CreateFailure = 2

class DatabaseUpdate(Enum):
    UpdateSuccess = 1
    UpdateFailure = 2

class DatabaseRemove(Enum):
    RemoveSuccess = 1
    RemoveFailure = 2

class UserDetails:
    def __init__(self, username: str, email: str, password: str, id: uuid.UUID):
        self.username = username
        self.email = email
        self.password = password
        self.id = id
