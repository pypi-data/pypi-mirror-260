from typing import Protocol

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from poaster.core import exceptions

from . import schemas, tables


class SupportsPostRepository(Protocol):
    """Interface for handling posts."""

    async def create(
        self, username: str, post: schemas.PostInputSchema
    ) -> schemas.PostSchema:
        """Create post after validating input schema."""
        ...

    async def update(
        self, id: int, post: schemas.PostInputSchema
    ) -> schemas.PostSchema:
        """Update post after validating input schema."""
        ...

    async def delete(self, id: int) -> schemas.PostSchema:
        """Delete post by id."""
        ...

    async def get_all(self) -> list[schemas.PostSchema]:
        """Fetch all posts from the DB."""
        ...

    async def get_by_id(self, id: int) -> schemas.PostSchema:
        """Fetch by id, raising exception if not found."""
        ...


class SqlalchemyPostRepository:
    """Implementation of the post repository with SqlAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self, username: str, post: schemas.PostInputSchema
    ) -> schemas.PostSchema:
        entry = tables.Post(**post.model_dump(), created_by=username)
        self._session.add(entry)
        await self._session.commit()
        return schemas.PostSchema.model_validate(entry)

    async def update(
        self, id: int, post: schemas.PostInputSchema
    ) -> schemas.PostSchema:
        if await self._session.get(tables.Post, id) is None:
            raise exceptions.DoesNotExist("Post doesn't exist.")

        qry = (
            update(tables.Post)
            .where(tables.Post.id == id)
            .values(title=post.title, text=post.text)
        )
        await self._session.execute(qry)
        await self._session.commit()

        db_post = await self._session.get(tables.Post, id)

        return schemas.PostSchema.model_validate(db_post)

    async def delete(self, id: int) -> schemas.PostSchema:
        if (post := await self._session.get(tables.Post, id)) is None:
            raise exceptions.DoesNotExist("Post doesn't exist.")

        qry = delete(tables.Post).where(tables.Post.id == post.id)
        await self._session.execute(qry)
        await self._session.commit()

        return schemas.PostSchema.model_validate(post)

    async def get_all(self) -> list[schemas.PostSchema]:
        qry = select(tables.Post).order_by(tables.Post.created_at.desc())
        results = await self._session.execute(qry)
        return [schemas.PostSchema.model_validate(res) for res in results.scalars()]

    async def get_by_id(self, id: int) -> schemas.PostSchema:
        if (post := await self._session.get(tables.Post, id)) is None:
            raise exceptions.DoesNotExist("Post doesn't exist.")

        return schemas.PostSchema.model_validate(post)


class SupportsPostVersionRepository(Protocol):
    """Interface for handling post versions."""

    async def create(
        self, *, username: str, post_id: int, post: schemas.PostInputSchema
    ) -> schemas.PostVersionSchema:
        """Create post version after validating input schema."""
        ...

    async def get_all(self, *, post_id: int) -> list[schemas.PostVersionSchema]:
        """Fetch all versions of a post from the DB."""
        ...

    async def get_by_id(
        self, *, post_id: int, version_id: int
    ) -> schemas.PostVersionSchema:
        """Fetch post version by id, raising exception if not found."""
        ...


class SqlalchemyPostVersionRepository:
    """Implementation of the post version repository with SqlAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self, *, username: str, post_id: int, post: schemas.PostInputSchema
    ) -> schemas.PostVersionSchema:
        qry = (
            select(tables.PostVersion)
            .where(tables.PostVersion.post_id == post_id)
            .order_by(tables.PostVersion.updated_at.desc())
        )
        result = await self._session.execute(qry)
        latest_version = result.scalars().first()

        next_version = (
            schemas.PostVersionSchema.model_validate(latest_version).version + 1
            if latest_version
            else 1
        )

        entry = tables.PostVersion(
            **post.model_dump(),
            post_id=post_id,
            updated_by=username,
            version=next_version,
        )

        self._session.add(entry)
        await self._session.commit()
        return schemas.PostVersionSchema.model_validate(entry)

    async def get_all(self, *, post_id: int) -> list[schemas.PostVersionSchema]:
        qry = (
            select(tables.PostVersion)
            .where(tables.PostVersion.post_id == post_id)
            .order_by(tables.PostVersion.updated_at)
        )
        results = await self._session.execute(qry)
        return [
            schemas.PostVersionSchema.model_validate(post_version)
            for post_version in results.scalars()
        ]

    async def get_by_id(
        self, *, post_id: int, version_id: int
    ) -> schemas.PostVersionSchema:
        qry = (
            select(tables.PostVersion)
            .where(tables.PostVersion.post_id == post_id)
            .where(tables.PostVersion.version == version_id)
        )
        result = await self._session.execute(qry)

        if (post_version := result.scalars().one_or_none()) is None:
            raise exceptions.DoesNotExist("Post version doesn't exist.")

        return schemas.PostVersionSchema.model_validate(post_version)
