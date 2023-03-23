import socketio
import uuid

from enum import Enum, StrEnum

class RegisterError(Enum):
    InvalidCredentials = 1

class ClientEvents(StrEnum):
    Register = "register"
    Login = "login"

class UserDetails:
    def __init__(self, username: str, email: str, password: str, id: uuid.UUID):
        self.username = username
        self.email = email
        self.password = password
        self.id = id

class UnknownUser:
    def __init__(self, client: socketio.Client) -> None:
        self.client = client
        self.id = uuid.uuid4()

client: socketio.Client = socketio.Client()
user: UnknownUser = UnknownUser(client)

class User(UnknownUser):
    def __init__(self, client: socketio.Client, id: uuid.UUID) -> None:
        self.client = client
        self.id = id

class Guest(UnknownUser):
    def __init__(self, client: socketio.Client, id: uuid.UUID) -> None:
        self.client = client
        self.id = id

    def register(self: UnknownUser, username: str, email: str, password: str) -> None:
        self.client.emit("register", data = UserDetails(username, email, password, self.id))

"""
Creates a connection to server under default port 3000
@param {socketio.Client} client - Client to connect
@param {int | None} port - Optional server port
@returns {socketio.Client} - Connected client
"""
def create_client_connection(client: socketio.Client, port: int | None) -> socketio.Client:
    client.connect("http://localhost" + str(port or 3000))
    return client

"""
Emits register event to register user
@param {socketio.Client} client - Client to register
@param {UserDetails} details - Details of user to register with
@param {RegisterError | None} error - Optional parameter to determine if error occurred in registration process
@returns {None}
"""
@client.event
def client_register(client: socketio.Client, details: UserDetails, error: RegisterError | None) -> None:
    match error:
        case RegisterError:
            # Handle Register Error
            return

        case None:
            client = User(details.id)
            return
