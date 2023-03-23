import socketio
import uuid

from source.types import ClientEvents, RegisterError, UserDetails

class User:
    def __init__(self, client: socketio.Client, id: uuid.UUID) -> None:
        self.client = client
        self.id = id

class Guest:
    def __init__(self, client: socketio.Client) -> None:
        self.client = client
        self.id = uuid.uuid4()

    def register(self, username: str, email: str, password: str) -> None:
        self.client.emit("register", data = { "username": username, "email": email, "password": password, "id": str(self.id) })

"""
Creates a connection to server under default port 3000
@param {socketio.Client} client - Client to connect
@param {int | None} port - Optional server port
@returns {socketio.Client} - Connected client
"""

def create_client_connection(client: socketio.Client, port: int | None) -> socketio.Client:
    client.connect("http://localhost:3000")
    return client

client: socketio.Client = socketio.Client()
client.connect("http://localhost:3000")
user: Guest = Guest(client)
user.register("jacob", "jacob@jacob", "jacob123")

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
