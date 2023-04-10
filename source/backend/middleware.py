# NOTE:
# Timezone of all datetime objects: UTC

from typing import Final
from authlib.jose import jwt, JWTClaims
from os import getenv
import logging

from source.universal.project_types import TokenError, TimeAuthorize

class Middleware:
    AUTHORIZATION_HEADER: Final[str] = "Authorization"

    def authorization_exist(headers: dict[str, str]) -> bool:
        return Middleware.AUTHORIZATION_HEADER in headers

    def valid_encoded_token(token: str) -> bool:
        decoded_token: JWTClaims = jwt.decode(token, getenv("JWT_SECRET"))
        try:
            decoded_token.validate()
            return True
        except:
            return False
