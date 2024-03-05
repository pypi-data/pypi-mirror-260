from pydantic import Field

from poaster.core.schemas import BaseSchema


class UserLoginSchema(BaseSchema):
    """Login credentials for a user."""

    username: str = Field(max_length=255)
    password: str = Field(max_length=255)


class UserRegistrationSchema(BaseSchema):
    """Login credentials used for registration."""

    username: str = Field(max_length=255)
    password: str = Field(max_length=512)


class UserSchema(BaseSchema):
    """User fetched from the persistence layer."""

    id: int
    username: str
    password: str


class UserPublicSchema(BaseSchema):
    """User info to return to public api (no sensitive info)."""

    username: str


class UserTokenPayload(BaseSchema):
    """Payload for user access token."""

    sub: str
    exp: int


class AccessToken(BaseSchema):
    """Generated access token payload (JWT)."""

    access_token: str
    token_type: str
