import asyncio
import logging

import poaster.access.repository
import poaster.access.schemas
import poaster.access.services
import poaster.bulletin.repository
import poaster.bulletin.schemas
import poaster.bulletin.services
from poaster.core import exceptions, sessions


async def load_fixtures():
    """Load test fixtures useful for local development."""
    async with sessions.async_session() as session:
        u_repo = poaster.access.repository.SqlalchemyUserRepository(session)
        p_repo = poaster.bulletin.repository.SqlalchemyPostRepository(session)
        pv_repo = poaster.bulletin.repository.SqlalchemyPostVersionRepository(session)

        await add_dummy_user(u_repo)
        await add_dummy_posts(p_repo, pv_repo)


async def add_dummy_user(
    user_repository: poaster.access.repository.SupportsUserRepository,
):
    try:
        await poaster.access.services.register_user(
            user_repository=user_repository,
            username="dummy",
            password="password",
        )
    except exceptions.AlreadyExists:
        logging.info("'dummy' user already exists with password equal to 'password'.")
    else:
        logging.info("Added 'dummy' user with password equal to 'password'.")


async def add_dummy_posts(
    post_repository: poaster.bulletin.repository.SupportsPostRepository,
    post_version_repository: poaster.bulletin.repository.SupportsPostVersionRepository,
):
    async def add_post(title: str, text: str):
        await poaster.bulletin.services.create_post(
            post_repository,
            post_version_repository,
            username="dummy",
            payload=poaster.bulletin.schemas.PostInputSchema(title=title, text=text),
        )

    await add_post("Penguins", "Penguins are a group of aquatic flightless birds.")
    await add_post("Tigers", "Tigers are the largest living cat species.")
    await add_post("Koalas", "Koala is is native to Australia.")

    logging.info("Added example dummy posts about animals.")


if __name__ == "__main__":
    asyncio.run(load_fixtures())
