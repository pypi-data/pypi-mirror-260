import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from poaster.access import repository, schemas
from poaster.access.services import create_access_token


@pytest.fixture(autouse=True)
async def add_testuser(db_session: AsyncSession):
    repo = repository.SqlalchemyUserRepository(db_session)
    user = schemas.UserLoginSchema(username="testuser", password="secret")
    await repo.create(user)


def test_generate_token_success(client: TestClient):
    payload = {"username": "testuser", "password": "secret"}
    response = client.post("/api/auth/token", data=payload)
    assert response.status_code == status.HTTP_200_OK


def test_generate_token_fails_with_bad_username(client: TestClient):
    payload = {"username": "notvalid", "password": "secret"}
    response = client.post("/api/auth/token", data=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}


def test_generate_token_fails_with_bad_password(client: TestClient):
    payload = {"username": "testuser", "password": "notvalid"}
    response = client.post("/api/auth/token", data=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}


@pytest.mark.parametrize(
    "payload",
    [
        pytest.param({}, id="empty payload"),
        pytest.param({"username": "testuser"}, id="only username"),
        pytest.param({"password": "secret"}, id="only password"),
        pytest.param({"foo": "bar"}, id="invalid fields"),
    ],
)
def test_generate_token_fails_with_invalid_payload(
    client: TestClient, payload: dict[str, str]
):
    response = client.post("/api/auth/token", data=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_fetch_current_user_success(client: TestClient):
    token = create_access_token(username="testuser")
    headers = {"authorization": f"Bearer {token}"}
    response = client.get("/api/auth/me", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"username": "testuser"}


def test_fetch_current_user_without_token_header_fails(client: TestClient):
    response = client.get("/api/auth/me", headers={})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}


def test_fetch_current_user_with_bad_header_fails(client: TestClient):
    headers = {"authorization": "Bearer blahblahblahblah"}
    response = client.get("/api/auth/me", headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}
