from flask import Flask, request
from authlib.jose import jwt
from os import getenv
from returns.result import Success, Failure
import logging

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

            match create_user(user_details, details["password"]):
                case Success(_):
                    logging.log(logging.INFO, "User successfully created.")
                    return {
                        "token": HTTPServer.encode_dict(vars(user_details)),
                        "code": "200",
                    }
                case Failure(_):
                    logging.warning(logging.ERROR, "User could not be created!")
                    return {
                        "token": "",
                        "code": "403"
                    }

    def route_init(self) -> None:
        self.register_route()
