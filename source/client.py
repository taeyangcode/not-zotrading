import socketio
import uuid

from types import ClientEvents, RegisterError

class UserDetails:
    def __init__(self, username: str, email: str, password: str, id: uuid.UUID):
        self.username = username
        self.email = email
        self.password = password
        self.id = id

class User:
    def __init__(self, client: socketio.Client, id: uuid.UUID) -> None:
        self.client = client
        self.id = id

class Guest:
    def __init__(self, client: socketio.Client, id: uuid.UUID) -> None:
        self.client = client
        self.id = id

    def register(self, username: str, email: str, password: str) -> None:
        self.client.emit(ClientEvents.Register, data = UserDetails(username, email, password, self.id))

"""
Creates a connection to server under default port 3000
@param {socketio.Client} client - Client to connect
@param {int | None} port - Optional server port
@returns {socketio.Client} - Connected client
"""

def create_client_connection(client: socketio.Client, port: int | None) -> socketio.Client:
    client.connect("http://localhost" + str(port or 3000))
    return client

client: socketio.Client = create_client_connection(socketio.Client(), 3000)
user: Guest = Guest(client)

"""
Emits register event to register user
@param {socketio.Client} client - Client to register
@param {UserDetails} details - Details of user to register with
@param {RegisterError | None} error - Optional parameter to determine if error occurred in registration process
@returns {None}
"""
@client.event
def register(client: socketio.Client, details: UserDetails, error: RegisterError | None) -> None:
    match error:
        case RegisterError.InvalidCredentials:
            # Handle Register Error
            return

        case None:
            client = User(details.id)
            return
