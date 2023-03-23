from enum import Enum, StrEnum

class RegisterError(Enum):
    InvalidCredentials = 1

class ClientEvents(StrEnum):
    Register = "register"
    Login = "login"
