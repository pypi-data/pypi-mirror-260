from typing import Optional

from poaster.bulletin import repository, schemas
from poaster.core import exceptions


async def create_post(
    post_repository: repository.SupportsPostRepository,
    post_verson_repository: repository.SupportsPostVersionRepository,
    *,
    username: str,
    payload: schemas.PostInputSchema,
) -> schemas.PostSchema:
    """Create a bulletin post from an authenticated user."""
    post = await post_repository.create(username, payload)

    await post_verson_repository.create(
        username=username,
        post_id=post.id,
        post=payload,
    )

    return post


async def update_post(
    post_repository: repository.SupportsPostRepository,
    post_version_repository: repository.SupportsPostVersionRepository,
    *,
    id: int,
    username: str,
    payload: schemas.PostInputSchema,
) -> Optional[schemas.PostSchema]:
    """Get a bulletin post by id."""
    try:
        post = await post_repository.update(id, payload)
    except exceptions.DoesNotExist:
        return None

    await post_version_repository.create(
        username=username,
        post_id=post.id,
        post=payload,
    )

    return post


async def delete_post(
    post_repository: repository.SupportsPostRepository, *, id: int
) -> Optional[schemas.PostSchema]:
    """Get a bulletin post by id."""
    try:
        post = await post_repository.delete(id)
    except exceptions.DoesNotExist:
        return None

    return post


async def get_post(
    post_repository: repository.SupportsPostRepository, *, id: int
) -> Optional[schemas.PostSchema]:
    """Get a bulletin post by id."""
    try:
        return await post_repository.get_by_id(id)
    except exceptions.DoesNotExist:
        return None


async def get_posts(
    post_repository: repository.SupportsPostRepository,
) -> list[schemas.PostSchema]:
    """Get a bulletin post by id."""
    return await post_repository.get_all()
