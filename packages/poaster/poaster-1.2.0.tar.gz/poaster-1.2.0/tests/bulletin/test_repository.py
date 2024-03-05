import datetime

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from poaster.bulletin import repository, schemas
from poaster.core import exceptions


@pytest.fixture
def post_repo(db_session: AsyncSession) -> repository.SqlalchemyPostRepository:
    return repository.SqlalchemyPostRepository(db_session)


@pytest.fixture
def post_version_repo(
    db_session: AsyncSession,
) -> repository.SqlalchemyPostVersionRepository:
    return repository.SqlalchemyPostVersionRepository(db_session)


async def test_create_post(post_repo: repository.SqlalchemyPostRepository):
    got = await post_repo.create(
        username="testuser",
        post=schemas.PostInputSchema(title="hi", text="hello, world!"),
    )
    want = schemas.PostSchema(
        id=1,
        title="hi",
        text="hello, world!",
        created_by="testuser",
        created_at=got.created_at,
    )

    assert got == want


async def test_update_post(
    db_session: AsyncSession, post_repo: repository.SupportsPostRepository
):
    qry = """
    INSERT INTO posts (title, text, created_by, created_at)
    VALUES ('hi', 'hello, world!', 'testuser', '2024-02-13 08:00');
    """
    await db_session.execute(text(qry))

    got = await post_repo.update(
        1, schemas.PostInputSchema(title="hi v2", text="hello, world!!")
    )
    want = schemas.PostSchema(
        id=got.id,
        title="hi v2",
        text="hello, world!!",
        created_by="testuser",
        created_at=datetime.datetime(2024, 2, 13, 8, 0),
    )

    assert got == want


async def test_delete_post_response(
    db_session: AsyncSession, post_repo: repository.SupportsPostRepository
):
    qry = """
    INSERT INTO posts (title, text, created_by, created_at)
    VALUES ('hi', 'hello, world!', 'testuser', '2024-02-13 08:00');
    """
    await db_session.execute(text(qry))

    got = await post_repo.delete(1)
    want = schemas.PostSchema(
        id=got.id,
        title="hi",
        text="hello, world!",
        created_by="testuser",
        created_at=datetime.datetime(2024, 2, 13, 8, 0),
    )

    assert got == want


async def test_delete_post_actually_deleted(
    db_session: AsyncSession, post_repo: repository.SupportsPostRepository
):
    qry = """
    INSERT INTO posts (title, text, created_by, created_at)
    VALUES ('hi', 'hello, world!', 'testuser', '2024-02-13 08:00');
    """
    await db_session.execute(text(qry))
    await post_repo.delete(1)
    with pytest.raises(exceptions.DoesNotExist, match="Post doesn't exist."):
        await post_repo.get_by_id(1)


async def test_delete_post_cascade_deletes_versions(
    db_session: AsyncSession,
    post_repo: repository.SupportsPostRepository,
    post_version_repo: repository.SupportsPostVersionRepository,
):
    add_post_qry = """
    INSERT INTO posts (title, text, created_by, created_at)
    VALUES ('hi', 'hello, world!', 'testuser', '2024-02-13 08:00');
    """
    await db_session.execute(text(add_post_qry))

    add_post_version_qry = """
    INSERT INTO post_versions (post_id, title, text, version, updated_by, updated_at)
    VALUES (1, 'hi', 'hello, world!', 1, 'testuser', '2024-02-13 08:00');
    """
    await db_session.execute(text(add_post_version_qry))

    await post_repo.delete(1)

    with pytest.raises(exceptions.DoesNotExist, match="Post version doesn't exist."):
        await post_version_repo.get_by_id(post_id=1, version_id=1)


async def test_get_post_by_id(
    db_session: AsyncSession, post_repo: repository.SupportsPostRepository
):
    qry = """
    INSERT INTO posts (title, text, created_by, created_at)
    VALUES ('hi', 'hello, world!', 'testuser', '2024-02-13 08:00');
    """
    await db_session.execute(text(qry))

    got = await post_repo.get_by_id(1)
    want = schemas.PostSchema(
        id=got.id,
        title="hi",
        text="hello, world!",
        created_by="testuser",
        created_at=datetime.datetime(2024, 2, 13, 8, 0),
    )

    assert got == want


async def test_post_not_found(post_repo: repository.SupportsPostRepository):
    with pytest.raises(exceptions.DoesNotExist, match="Post doesn't exist."):
        await post_repo.get_by_id(42)


async def test_get_all_posts(
    db_session: AsyncSession, post_repo: repository.SupportsPostRepository
):
    qry = """
    INSERT INTO posts (title, text, created_by, created_at)
    VALUES
        ('oldest_post', 'hello, oldest_post!', 'testuser', '2024-02-13 08:00'),
        ('newest_post', 'hello, newest_post!', 'testuser', '2024-02-15 12:00')
    ;
    """
    await db_session.execute(text(qry))

    got = await post_repo.get_all()
    want = [
        schemas.PostSchema(
            id=2,
            title="newest_post",
            text="hello, newest_post!",
            created_by="testuser",
            created_at=datetime.datetime(2024, 2, 15, 12, 0),
        ),
        schemas.PostSchema(
            id=1,
            title="oldest_post",
            text="hello, oldest_post!",
            created_by="testuser",
            created_at=datetime.datetime(2024, 2, 13, 8, 0),
        ),
    ]

    assert got == want


async def test_get_all_none_found(post_repo: repository.SupportsPostRepository):
    got = await post_repo.get_all()
    want = []

    assert got == want


async def test_create_post_version_v1(
    db_session: AsyncSession,
    post_version_repo: repository.SqlalchemyPostVersionRepository,
):
    add_post_qry = """
    INSERT INTO posts (title, text, created_by, created_at)
    VALUES ('hi', 'hello, world!', 'testuser', '2024-02-13 08:00');
    """
    await db_session.execute(text(add_post_qry))

    got = await post_version_repo.create(
        username="testuser",
        post_id=1,
        post=schemas.PostInputSchema(title="hi", text="hello, world!"),
    )
    want = schemas.PostVersionSchema(
        id=1,
        post_id=1,
        title="hi",
        text="hello, world!",
        version=1,
        updated_by="testuser",
        updated_at=got.updated_at,
    )

    assert got == want


async def test_create_post_version_v2(
    db_session: AsyncSession,
    post_version_repo: repository.SqlalchemyPostVersionRepository,
):
    add_post_qry = """
    INSERT INTO posts (title, text, created_by, created_at)
    VALUES ('hi', 'hello, world!', 'testuser', '2024-02-13 08:00');
    """
    await db_session.execute(text(add_post_qry))

    add_post_version_qry = """
    INSERT INTO post_versions (post_id, title, text, version, updated_by, updated_at)
    VALUES (1, 'hi', 'hello, world!', 1, 'testuser', '2024-02-13 08:00');
    """
    await db_session.execute(text(add_post_version_qry))

    got = await post_version_repo.create(
        username="testuser",
        post_id=1,
        post=schemas.PostInputSchema(title="hi", text="hello, world!"),
    )
    want = schemas.PostVersionSchema(
        id=2,
        post_id=1,
        title="hi",
        text="hello, world!",
        version=2,
        updated_by="testuser",
        updated_at=got.updated_at,
    )

    assert got == want


async def test_get_all_post_versions(
    db_session: AsyncSession,
    post_version_repo: repository.SqlalchemyPostVersionRepository,
):
    add_post_qry = """
    INSERT INTO posts (title, text, created_by, created_at)
    VALUES ('hi', 'hello, world!', 'testuser', '2024-02-13 08:00');
    """
    await db_session.execute(text(add_post_qry))

    add_post_versions_qry = """
    INSERT INTO post_versions (post_id, title, text, version, updated_by, updated_at)
    VALUES
      (1, 'hi v1', 'hello, world!', 1, 'testuser', '2024-02-13 08:00'),
      (1, 'hi v2', 'hello, world!!', 2, 'testuser', '2024-02-13 09:00'),
      (1, 'hi v3', 'hello, world!!!', 3, 'testuser', '2024-02-13 10:00')
    ;
    """
    await db_session.execute(text(add_post_versions_qry))

    got = await post_version_repo.get_all(post_id=1)
    want = [
        schemas.PostVersionSchema(
            id=1,
            post_id=1,
            title="hi v1",
            text="hello, world!",
            version=1,
            updated_by="testuser",
            updated_at=datetime.datetime(2024, 2, 13, 8),
        ),
        schemas.PostVersionSchema(
            id=2,
            post_id=1,
            title="hi v2",
            text="hello, world!!",
            version=2,
            updated_by="testuser",
            updated_at=datetime.datetime(2024, 2, 13, 9),
        ),
        schemas.PostVersionSchema(
            id=3,
            post_id=1,
            title="hi v3",
            text="hello, world!!!",
            version=3,
            updated_by="testuser",
            updated_at=datetime.datetime(2024, 2, 13, 10),
        ),
    ]

    assert got == want


async def test_get_post_version_by_id(
    db_session: AsyncSession,
    post_version_repo: repository.SqlalchemyPostVersionRepository,
):
    add_post_qry = """
    INSERT INTO posts (title, text, created_by, created_at)
    VALUES ('hi', 'hello, world!', 'testuser', '2024-02-13 08:00');
    """
    await db_session.execute(text(add_post_qry))

    add_post_versions_qry = """
    INSERT INTO post_versions (post_id, title, text, version, updated_by, updated_at)
    VALUES
      (1, 'hi v1', 'hello, world!', 1, 'testuser', '2024-02-13 08:00'),
      (1, 'hi v2', 'hello, world!!', 2, 'testuser', '2024-02-13 09:00'),
      (1, 'hi v3', 'hello, world!!!', 3, 'testuser', '2024-02-13 10:00')
    ;
    """
    await db_session.execute(text(add_post_versions_qry))

    got = await post_version_repo.get_by_id(post_id=1, version_id=2)
    want = schemas.PostVersionSchema(
        id=2,
        post_id=1,
        title="hi v2",
        text="hello, world!!",
        version=2,
        updated_by="testuser",
        updated_at=datetime.datetime(2024, 2, 13, 9),
    )

    assert got == want
