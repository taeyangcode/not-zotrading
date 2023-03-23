from enum import Enum, StrEnum
import uuid
class RegisterError(Enum):
    InvalidCredentials = 1

class ClientEvents(StrEnum):
    Register = "register"
    Login = "login"

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