from collections.abc import AsyncGenerator

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated

import poaster.access.repository
import poaster.bulletin.repository
from poaster.core import exceptions, http_exceptions, oauth, sessions

AuthBearer = Annotated[oauth.Token, Depends(oauth.oauth2_scheme)]
AuthForm = Annotated[OAuth2PasswordRequestForm, Depends()]


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session, commiting changes before closing."""
    async with sessions.async_session() as session:
        yield session
        await session.commit()


DBSession = Annotated[AsyncSession, Depends(get_db_session)]


def get_post_repository(
    db_session: DBSession,
) -> poaster.bulletin.repository.SqlalchemyPostRepository:
    """Instantiate post repository session."""
    return poaster.bulletin.repository.SqlalchemyPostRepository(db_session)


PostRepository = Annotated[
    poaster.bulletin.repository.SupportsPostRepository, Depends(get_post_repository)
]


def get_post_version_repository(
    db_session: DBSession,
) -> poaster.bulletin.repository.SqlalchemyPostVersionRepository:
    """Instantiate post version repository session."""
    return poaster.bulletin.repository.SqlalchemyPostVersionRepository(db_session)


PostVersionRepository = Annotated[
    poaster.bulletin.repository.SupportsPostVersionRepository,
    Depends(get_post_version_repository),
]


def get_user_repository(
    db_session: DBSession,
) -> poaster.access.repository.SqlalchemyUserRepository:
    """Instantiate user repository session."""
    return poaster.access.repository.SqlalchemyUserRepository(db_session)


UserRepository = Annotated[
    poaster.access.repository.SupportsUserRepository, Depends(get_user_repository)
]


def get_current_username(token: AuthBearer) -> str:
    """Try and retrieve username based on passed token."""
    try:
        payload = oauth.decode_token(token)
    except exceptions.Unauthorized as err:
        raise http_exceptions.InvalidCredentials from err
    else:
        return str(payload.get("sub", ""))


CurrentUsername = Annotated[str, Depends(get_current_username)]
