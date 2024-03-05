from collections.abc import AsyncGenerator

import pytest
from click.testing import CliRunner
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from sqlalchemy.ext.asyncio.session import AsyncSession


@pytest.fixture(scope="session", autouse=True)
async def db_engine() -> AsyncGenerator[AsyncEngine, None]:
    from poaster.core import sessions, tables

    async with sessions.async_engine.begin() as conn:
        await conn.run_sync(tables.Base.metadata.create_all)

    yield sessions.async_engine

    async with sessions.async_engine.begin() as conn:
        await conn.run_sync(tables.Base.metadata.drop_all)


@pytest.fixture
async def db_session(db_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    """Database session that will rolled back after test run."""
    from poaster.core import tables

    async with async_sessionmaker(db_engine, expire_on_commit=False)() as session:
        yield session
        await session.rollback()

        for table in reversed(tables.Base.metadata.sorted_tables):
            await session.execute(text(f"DELETE FROM {table.name};"))
            await session.commit()


@pytest.fixture(scope="session")
def client() -> TestClient:
    """Test client (httpx) fixture for making requests to the app."""
    from poaster.app import app

    return TestClient(app)


@pytest.fixture(scope="session")
def cli_runner() -> CliRunner:
    return CliRunner()
