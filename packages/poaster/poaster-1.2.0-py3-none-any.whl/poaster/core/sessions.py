from sqlalchemy import event
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from poaster.core.config import settings

engine = create_engine(settings.uri)
async_engine = create_async_engine(settings.async_uri)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)


@event.listens_for(async_engine.sync_engine, "connect")
def set_sqlite_pragma(dbapi_connection, _) -> None:  # type: ignore
    """Set sqlite settings before instantiating a connection."""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
