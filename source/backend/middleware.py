# NOTE:
# Timezone of all datetime objects: UTC

from typing import Final
from authlib.jose import jwt, JWTClaims
from os import getenv

from source.universal.project_types import TokenError

class AuthorizationMiddleware:
    AUTHORIZATION_HEADER: Final[str] = "Authorization"

    def authorization_exist(headers: dict[str, str]) -> bool:
        return AuthorizationMiddleware.AUTHORIZATION_HEADER in headers

    def valid_encoded_token(token: str) -> bool:
        decoded_token: JWTClaims = jwt.decode(token, getenv("JWT_SECRET"))
