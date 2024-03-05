from typing import Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from poaster.access.services import create_access_token

Headers = dict[str, str]
"""Helper alias for request header (only for testing)."""

Payload = dict[str, Any]
"""Helper alias for request payload (only for testing)."""


@pytest.fixture
async def add_example_posts(db_session: AsyncSession) -> None:
    qry = """
    INSERT INTO posts (title, text, created_by, created_at)
    VALUES
        ('oldest_post', 'hello, oldest_post!', 'testuser', '2024-02-13 08:00'),
        ('newest_post', 'hello, newest_post!', 'testuser', '2024-02-15 12:00')
    ;
    """
    await db_session.execute(text(qry))


@pytest.fixture
def headers() -> Headers:
    token = create_access_token(username="testuser")
    return {"authorization": f"Bearer {token}"}


def test_create_post(client: TestClient, headers: Headers):
    payload = {"title": "hi", "text": "hello, world!"}
    response = client.post("/api/posts", headers=headers, json=payload)
    assert response.status_code == status.HTTP_201_CREATED


def test_create_post_unauthorized(client: TestClient):
    payload = {"title": "hi", "text": "hello, world!"}
    response = client.post("/api/posts", data=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize(
    "payload",
    [
        pytest.param({}, id="empty payload"),
        pytest.param({"title": "hi"}, id="only title"),
        pytest.param({"text": "hello, world!"}, id="only text"),
        pytest.param({"title": 1, "text": "hello, world!"}, id="bad title"),
        pytest.param({"title": "hi", "text": 1}, id="bad text"),
        pytest.param({"title": "hi" * 1000, "text": "hello"}, id="too long of a title"),
    ],
)
def test_create_post_with_bad_payload(
    client: TestClient, headers: Headers, payload: Payload
):
    response = client.post("/api/posts", headers=headers, json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.usefixtures("add_example_posts")
def test_update_post(client: TestClient, headers: Headers):
    payload = {"title": "hi v2", "text": "hello, world!!"}
    response = client.put("/api/posts/1", headers=headers, json=payload)
    assert response.status_code == status.HTTP_200_OK


def test_update_post_not_found(client: TestClient, headers: Headers):
    payload = {"title": "hi v2", "text": "hello, world!!"}
    response = client.put("/api/posts/42", headers=headers, json=payload)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_post_unauthorized(client: TestClient):
    payload = {"title": "hi", "text": "hello, world!"}
    response = client.put("/api/posts/1", data=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize(
    "payload",
    [
        pytest.param({}, id="empty payload"),
        pytest.param({"title": "hi"}, id="only title"),
        pytest.param({"text": "hello, world!"}, id="only text"),
        pytest.param({"title": 1, "text": "hello, world!"}, id="bad title"),
        pytest.param({"title": "hi", "text": 1}, id="bad text"),
        pytest.param({"title": "hi" * 1000, "text": "hello"}, id="too long of a title"),
    ],
)
def test_update_post_with_bad_payload(
    client: TestClient, headers: Headers, payload: Payload
):
    response = client.put("/api/posts/1", headers=headers, json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.usefixtures("add_example_posts")
def test_delete_post(client: TestClient, headers: Headers):
    response = client.delete("/api/posts/1", headers=headers)
    assert response.status_code == status.HTTP_200_OK


def test_delete_post_not_found(client: TestClient, headers: Headers):
    response = client.delete("/api/posts/42", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_post_unauthorized(client: TestClient):
    response = client.delete("/api/posts/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.usefixtures("add_example_posts")
def test_get_post(client: TestClient):
    response = client.get("/api/posts/1")
    assert response.status_code == status.HTTP_200_OK


def test_get_post_not_found(client: TestClient):
    response = client.get("/api/posts/42")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.usefixtures("add_example_posts")
def test_get_posts(client: TestClient):
    response = client.get("/api/posts/1")
    assert response.status_code == status.HTTP_200_OK
