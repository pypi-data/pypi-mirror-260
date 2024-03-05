from fastapi import APIRouter

from poaster import dependencies
from poaster.core import http_exceptions

from . import schemas, services

router = APIRouter(prefix="/auth", tags=["access"])


@router.post("/token", summary="Generates access token when passed valid credentials.")
async def handle_generate_access_token(
    form: dependencies.AuthForm,
    user_repository: dependencies.UserRepository,
) -> schemas.AccessToken:
    """Defines endpoint for generating access tokens."""
    user = await services.authenticate(user_repository, form.username, form.password)

    if user is None:
        raise http_exceptions.InvalidCredentials

    token = services.create_access_token(user.username)

    return schemas.AccessToken(access_token=token, token_type="bearer")


@router.get("/me", summary="Fetches information regarding current user.")
async def handle_get_current_user(
    username: dependencies.CurrentUsername,
    user_repository: dependencies.UserRepository,
) -> schemas.UserPublicSchema:
    """Defines endpoint for fetching information for the current user."""
    if await services.check_username_exists(user_repository, username):
        return schemas.UserPublicSchema(username=username)

    raise http_exceptions.InvalidCredentials
