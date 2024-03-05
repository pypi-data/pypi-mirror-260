import datetime
from typing import Optional

from poaster.core import exceptions, hashing, oauth

from . import repository, schemas


async def authenticate(
    user_repository: repository.SupportsUserRepository, username: str, password: str
) -> Optional[schemas.UserSchema]:
    """Check that input credentials match the user's stored credentials."""
    try:
        user = await user_repository.get_by_username(username)
    except exceptions.DoesNotExist:
        return None

    if not hashing.pwd_context.verify(password, user.password):
        return None

    return user


def create_access_token(username: str, minutes: int = 60) -> oauth.Token:
    """Generate user access token for a duration of time."""
    payload: oauth.TokenPayload = {
        "sub": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=minutes),
    }
    return oauth.encode_token(payload)


def decode_access_token(token: oauth.Token) -> schemas.UserTokenPayload:
    """Decode user access token."""
    payload = oauth.decode_token(token)
    return schemas.UserTokenPayload.model_validate(payload)


async def check_username_exists(
    user_repository: repository.SupportsUserRepository, username: str
) -> bool:
    """Check if username exists."""
    try:
        await user_repository.get_by_username(username)
    except exceptions.DoesNotExist:
        return False
    else:
        return True


async def register_user(
    user_repository: repository.SupportsUserRepository, username: str, password: str
) -> schemas.UserSchema:
    """Register user given valid username and password."""
    user = schemas.UserRegistrationSchema(username=username, password=password)
    return await user_repository.create(user)


async def list_usernames(
    user_repository: repository.SupportsUserRepository,
) -> list[str]:
    """List out all persisted usernames."""
    users = await user_repository.get_all()
    return [user.username for user in users]
