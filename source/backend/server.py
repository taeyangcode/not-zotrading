from flask import Flask, request
from authlib.jose import jwt
from os import getenv

from source.universal.project_types import UserDetails
from source.backend.database import create_user

class HTTPServer:
    def __init__(self, server: Flask) -> None:
        self.server = server
        self.route_init()

    def encode_dict(dict: dict[any, any]) -> str:
        return jwt.encode(
            header = { "alg": "HS256", "typ": "JWT" },
            payload = dict,
            key = getenv("JWT_SECRET")
        ).decode("utf-8")

    def register_route(self) -> dict[str, str]:
        @self.server.route("/api/v1/register/", methods=[ "POST" ])
        def register_account() -> bytes:
            details = request.get_json()
            user_details = UserDetails(
                username = details["username"],
                email = details["email"],
                id = details["id"]
            )
            create_user(user_details, details["password"])
            return {
                "token": HTTPServer.encode_dict(vars(user_details))
            }

    def route_init(self):
        self.register_route()
