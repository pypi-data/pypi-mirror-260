from fastapi import APIRouter
from starlette.status import HTTP_201_CREATED

from poaster import dependencies
from poaster.core import http_exceptions

from . import schemas, services

router = APIRouter(tags=["bulletin"])


@router.post(
    "/posts",
    status_code=HTTP_201_CREATED,
    summary="Creates post when passed valid input.",
)
async def handle_create_post(
    payload: schemas.PostInputSchema,
    username: dependencies.CurrentUsername,
    post_repository: dependencies.PostRepository,
    post_version_repository: dependencies.PostVersionRepository,
) -> schemas.PostSchema:
    """Defines endpoint for creating bulletin posts."""
    return await services.create_post(
        post_repository,
        post_version_repository,
        username=username,
        payload=payload,
    )


@router.put("/posts/{id}", summary="Update post by id.")
async def handle_update_post(
    id: int,
    payload: schemas.PostInputSchema,
    username: dependencies.CurrentUsername,
    post_repository: dependencies.PostRepository,
    post_version_repository: dependencies.PostVersionRepository,
) -> schemas.PostSchema:
    """Defines endpoint for updating a post."""
    post = await services.update_post(
        post_repository,
        post_version_repository,
        id=id,
        username=username,
        payload=payload,
    )

    if post is None:
        raise http_exceptions.NotFound

    return post


@router.delete("/posts/{id}", summary="Delete post by id.")
async def handle_delete_post(
    id: int,
    _: dependencies.CurrentUsername,
    post_repository: dependencies.PostRepository,
) -> schemas.PostSchema:
    """Defines endpoint for deleting a post."""
    if (post := await services.delete_post(post_repository, id=id)) is None:
        raise http_exceptions.NotFound

    return post


@router.get("/posts", summary="Get all posts.")
async def handle_get_posts(
    post_repository: dependencies.PostRepository,
) -> list[schemas.PostSchema]:
    """Defines endpoint for retrieving all posts."""
    return await services.get_posts(post_repository)


@router.get("/posts/{id}", summary="Get post by id.")
async def handle_get_post(
    id: int,
    post_repository: dependencies.PostRepository,
) -> schemas.PostSchema:
    """Defines endpoint for retrieving a post by its id."""
    if (post := await services.get_post(post_repository, id=id)) is None:
        raise http_exceptions.NotFound

    return post
