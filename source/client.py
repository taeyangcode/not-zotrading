import socketio
import uuid
from typing_extensions import Self
from source.project_types import RegisterError, UserDetails

class User:
    def __init__(self, client: socketio.Client, id: uuid.UUID) -> None:
        self.client = client
        self.id = id

    def delete_account(self):
        self.client.emit("delete_account", data = { "id": str(self.id) })

class Guest:
    def __init__(self, client: socketio.Client) -> None:
        self.client = client
        self.id = uuid.uuid4()
        self.client_setup()

    def client_setup(self):
        """
        Emits register event to register user
        @param {socketio.Client} client - Client to register
        @param {UserDetails} details - Details of user to register with
        @param {RegisterError | None} error - Optional parameter to determine if error occurred in registration process
        @returns {None}
        """
        @self.client.event
        def register(client: socketio.Client, details: UserDetails, error: RegisterError | None) -> None:
            match error:
                case RegisterError.InvalidCredentials:
                    # Handle Register Error
                    return

                case None:
                    client = User(details.id)
                    return

    def register(self, username: str, email: str, password: str) -> Self | User:
        print(self.client.emit(
            "register",
            data = {
                "username": username,
                "email": email,
                "password": password,
                "id": str(self.id)
            },
            callback = lambda register_result: register_result
        ))

"""
Creates a connection to server under default port 3000
@param {socketio.Client} client - Client to connect
@param {int | None} port - Optional server port
@returns {socketio.Client} - Connected client
"""
def create_client_connection(client: socketio.Client, port: int | None = None) -> socketio.Client:
    client.connect("http://localhost:" + str(port or 3000))
    return client
