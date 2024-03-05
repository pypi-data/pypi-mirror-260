import datetime

from pydantic import Field

from poaster.core.schemas import BaseSchema


class PostInputSchema(BaseSchema):
    """Post input from user."""

    title: str = Field(max_length=255)
    text: str


class PostSchema(BaseSchema):
    """Post fetched from the persistence layer."""

    id: int
    title: str
    text: str
    created_by: str
    created_at: datetime.datetime


class PostVersionSchema(BaseSchema):
    """Post version fetched from the persistence layer."""

    id: int
    post_id: int
    title: str
    text: str
    version: int
    updated_by: str
    updated_at: datetime.datetime
