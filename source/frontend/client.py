from socketio import Client
from uuid import uuid4
from typing_extensions import Self
from requests import post
from returns.result import Success, Failure, Result
import logging

from source.universal.project_types import ServerConnectionError

class User:
    def __init__(self, client: Client, token: bytes) -> None:
        self.client = client
        self.token = token

    # def delete_account(self):

class Guest:
    def __init__(self, client: Client) -> None:
        self.client = client

    def register(self, username: str, email: str, password: str) -> Result[User, Self]:
        def try_register() -> Result[str, None]:
            try:
                url: str = "http://localhost:5000/api/v1/register/"
                json: dict[str, str] = {
                    "username": username,
                    "email": email,
                    "password": password,
                    "id": uuid4()
                }
                register_response: dict[str, str] = post(url, json=json).json()
                match register_response["code"]:
                    case "200":
                        return Success(register_response["token"])
                    case "403":
                        return Failure(None)
                    case _:
                        return Failure(None)
            except:
                return None

        match try_register():
            case Success(user_token):
                return User(self.client, user_token)
            case Failure(_):
                return Self

"""
Creates a connection to server under default port 3000
@param {socketio.Client} client - Client to connect
@param {int | None} port - Optional server port
@returns {socketio.Client} - Connected client
"""
def create_client_connection(client: Client, port: str | None = "6000") -> Result[(), ServerConnectionError]:
    try:
        client.connect("http://localhost:" + port)
    except:
        logging.warning("Could not connect to http://localhost:" + port)
