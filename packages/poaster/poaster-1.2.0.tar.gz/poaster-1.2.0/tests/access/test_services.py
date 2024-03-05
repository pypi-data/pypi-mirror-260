import datetime

import pydantic
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from poaster.access import repository, schemas, services
from poaster.core import exceptions, oauth


@pytest.fixture
def user_repo(db_session: AsyncSession) -> repository.SqlalchemyUserRepository:
    return repository.SqlalchemyUserRepository(db_session)


@pytest.fixture
async def user(
    user_repo: repository.SupportsUserRepository,
) -> schemas.UserSchema:
    return await user_repo.create(
        schemas.UserRegistrationSchema(username="bob", password="password")
    )


async def test_authenticate_success(
    user_repo: repository.SupportsUserRepository, user: schemas.UserSchema
):
    got = await services.authenticate(user_repo, user.username, "password")
    want = user

    assert got == want


async def test_authenticate_bad_username(
    user_repo: repository.SupportsUserRepository,
):
    got = await services.authenticate(user_repo, "badusername", "password")
    want = None

    assert got == want


async def test_authenticate_bad_pw(
    user_repo: repository.SupportsUserRepository, user: schemas.UserSchema
):
    got = await services.authenticate(user_repo, user.username, "badpw")
    want = None

    assert got == want


def test_encoding_and_decoding_of_user_access_token(user: schemas.UserSchema):
    now_in_secs = int(datetime.datetime.now().strftime("%s"))

    token = services.create_access_token(username=user.username, minutes=1)
    payload = services.decode_access_token(token)

    assert payload.sub == user.username  # subject is username
    assert payload.exp - now_in_secs == 60  # expiration is 1 minute


def test_wrongly_formatted_token_raises_unauthorized():
    token = oauth.Token("blahblahblahblahIamatokenhaha")

    with pytest.raises(exceptions.Unauthorized):
        services.decode_access_token(token)


def test_wrong_payload_field_raises_validation_error():
    token = oauth.encode_token(
        {
            "sub": "bob",
            "iss": "me",  # 'iss' field is not part of the access token schema
        }
    )

    with pytest.raises(pydantic.ValidationError):
        services.decode_access_token(token)


@pytest.mark.parametrize(
    "creds",
    [
        pytest.param(("testuser", "password" * 100), id="password too long"),
        pytest.param(("testuser" * 100, "password"), id="username too long"),
    ],
)
async def test_register_user_validation(
    user_repo: repository.SupportsUserRepository, creds: tuple[str, str]
):
    username, password = creds
    with pytest.raises(pydantic.ValidationError):
        await services.register_user(user_repo, username, password)


async def test_register_user_and_list_usernames(
    user_repo: repository.SupportsUserRepository,
):
    await services.register_user(user_repo, "testuser", "password")

    got = await services.list_usernames(user_repo)
    want = ["testuser"]

    assert got == want


async def test_register_user_already_exists(
    user_repo: repository.SupportsUserRepository,
):
    await services.register_user(user_repo, "testuser", "password")

    got = await services.check_username_exists(user_repo, "testuser")
    want = True

    assert got == want


async def test_check_username_does_not_exists(
    user_repo: repository.SupportsUserRepository,
):
    await services.register_user(user_repo, "testuser", "password")

    got = await services.check_username_exists(user_repo, "baduser")
    want = False

    assert got == want
