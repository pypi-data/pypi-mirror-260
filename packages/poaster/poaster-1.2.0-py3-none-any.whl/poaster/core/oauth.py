from typing import Any, NewType

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from . import config, exceptions

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


Token = NewType("Token", str)
"""Represents an encoded JWT string."""

TokenPayload = dict[str, Any]
"""Alias for token payload encoded in JWT."""


def encode_token(payload: TokenPayload) -> Token:
    """Encode token payload using secret key and algorithm."""
    jwt_token = jwt.encode(
        payload,
        key=config.settings.secret_key,
        algorithm=config.settings.algorithm,
    )
    return Token(jwt_token)


def decode_token(token: Token) -> TokenPayload:
    """Decode token using secret key and algorithm."""
    try:
        return jwt.decode(
            token=token,
            key=config.settings.secret_key,
            algorithms=[config.settings.algorithm],
        )
    except JWTError as err:
        raise exceptions.Unauthorized from err
