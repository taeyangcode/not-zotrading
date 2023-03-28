from socketio import Client
from uuid import UUID, uuid4
from typing_extensions import Self
from requests import post

from source.universal.project_types import RegisterError, UserDetails

class User:
    def __init__(self, client: Client, token: bytes) -> None:
        self.client = client
        self.token = token

    # def delete_account(self):

class Guest:
    def __init__(self, client: Client) -> None:
        self.client = client

    def register(self, username: str, email: str, password: str) -> Self | User:
        def try_register():
            try:
                register_response = post(
                    url = "http://localhost:5000/api/v1/register/",
                    data = {
                        "username": username,
                        "email": email,
                        "password": password,
                        "id": uuid4()
                    }
                ).json()
                return register_response["token"]
            except:
                return None
        user_token = try_register()
        if user_token is not None:
            return User(self.client, user_token)
        return self

"""
Creates a connection to server under default port 3000
@param {socketio.Client} client - Client to connect
@param {int | None} port - Optional server port
@returns {socketio.Client} - Connected client
"""
def create_client_connection(client: Client, port: int | None = None) -> Client:
    try:
        client.connect("http://localhost:" + str(port or 6000))
    except:
        print("Could not connect to http://localhost:" + str(port or 6000))
    return client
