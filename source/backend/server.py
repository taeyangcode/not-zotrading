from flask import Flask, request
from authlib.jose import jwt
from os import getenv
from returns.result import Success, Failure
from uuid import uuid4
import logging

from source.universal.project_types import UserDetails, TimeAuthorize
from source.backend.database import create_user
from source.backend.middleware import Middleware

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
                id = uuid4(),
                exp = TimeAuthorize.create_expirey_time()
            )

            match create_user(user_details, details["password"]):
                case Success(_):
                    logging.log(logging.INFO, "User successfully created.")
                    return {
                        "token": HTTPServer.encode_dict(user_details.to_dict()),
                        "code": "200",
                        "message": "User successfully created."
                    }
                case Failure(_):
                    logging.warning(logging.ERROR, "User could not be created.")
                    return {
                        "token": "",
                        "code": "403",
                        "message": "User could not be created."
                    }

    def user_route(self) -> dict[str, str]:
        @self.server.route("/api/v1/user", methods = [ "GET" ])
        def handle_user_route() -> bytes:
            user_details: dict[str, str] = request.get_json()

            if "token" not in user_details:
                return {
                    "token": "",
                    "code": "403",
                    "message": "User token not supplied."
                }

            if Middleware.valid_encoded_token(user_details["token"]):
                return {
                    "token": user_details["token"],
                    "code": "200",
                    "message": "User validated."
                }
            return {
                "token": user_details["token"],
                "code": "403",
                "message": "Invalid token."
            }

    def route_init(self) -> None:
        self.register_route()
        self.user_route()
