from flask import Flask, request
from authlib.jose import jwt
from os import getenv

from source.universal.project_types import UserDetails
from source.backend.database import create_user

class HTTPServer:
    def __init__(self, server: Flask) -> None:
        self.server = server
        self.route_init()

    def register_route(self) -> None:
        @self.server.route("/api/v1/register/", methods=[ "POST" ])
        def register_account() -> bytes:
            details = request.form
            user_details = UserDetails(
                    username = details["username"],
                    email = details["email"],
                    id = details["id"]
            )
            create_user(user_details, details["password"])
            return {
                "token": jwt.encode(
                    header = { "alg": "HS256", "typ": "JWT" },
                    payload = user_details.__dict__,
                    key = getenv("JWT_SECRET")
                ).decode("utf-8")
            }

    def route_init(self):
        self.register_route()
