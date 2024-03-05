import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from poaster.access import repository, schemas
from poaster.core import exceptions


@pytest.fixture
def user_repo(db_session: AsyncSession) -> repository.SqlalchemyUserRepository:
    return repository.SqlalchemyUserRepository(db_session)


async def test_create_user_hashes_password(
    user_repo: repository.SupportsUserRepository,
):
    user = schemas.UserRegistrationSchema(username="bob", password="password")
    db_user = await user_repo.create(user)
    assert db_user.username == "bob"
    assert db_user.password.startswith("$argon2")


async def test_can_create_user(user_repo: repository.SupportsUserRepository):
    user = schemas.UserRegistrationSchema(username="bob", password="password")

    got = await user_repo.create(user)
    want = schemas.UserSchema(
        id=got.id,
        username="bob",
        password=got.password,  # dynamically hashed password
    )

    assert got == want


async def test_duplicate_user_raises(user_repo: repository.SupportsUserRepository):
    user = schemas.UserRegistrationSchema(username="bob", password="password")
    await user_repo.create(user)
    with pytest.raises(exceptions.AlreadyExists):
        await user_repo.create(user)


async def test_user_is_found_by_username(
    db_session: AsyncSession, user_repo: repository.SupportsUserRepository
):
    qry = "INSERT INTO users (username, password) VALUES ('bob', 'hashedpw');"
    await db_session.execute(text(qry))

    got = await user_repo.get_by_username("bob")
    want = schemas.UserSchema(
        id=got.id,
        username="bob",
        password="hashedpw",
    )

    assert got == want


async def test_user_is_not_found_by_username(
    user_repo: repository.SupportsUserRepository,
):
    with pytest.raises(exceptions.DoesNotExist):
        await user_repo.get_by_username("nobody")


async def test_get_all_users(
    db_session: AsyncSession, user_repo: repository.SupportsUserRepository
):
    qry = "INSERT INTO users (username, password) VALUES ('bob', 'hashedpw');"
    await db_session.execute(text(qry))

    got = await user_repo.get_all()
    want = [schemas.UserSchema(id=1, username="bob", password="hashedpw")]

    assert got == want


async def test_get_all_users_none_found(user_repo: repository.SupportsUserRepository):
    got = await user_repo.get_all()
    want = []

    assert got == want
