"""Add post versions table.

Revision ID: 34b9b6b1c9a3
Revises: 821b409e627c
Create Date: 2024-03-02 17:19:54.189806

"""
import asyncio
import logging

import sqlalchemy as sa
from alembic import op

from poaster.bulletin import repository, schemas
from poaster.core import exceptions, sessions

# revision identifiers, used by Alembic.
revision = "34b9b6b1c9a3"
down_revision = "821b409e627c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "post_versions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("post_id", sa.Integer(), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("updated_by", sa.String(length=255), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["post_id"], ["posts.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("post_id", "version", name="unique_post_version"),
    )
    asyncio.run(initialize_post_versions())


def downgrade() -> None:
    op.drop_table("post_versions")


async def initialize_post_versions() -> None:
    """Initialize existing posts with with version 1."""
    async with sessions.async_session() as session:
        post_repo = repository.SqlalchemyPostRepository(session)
        post_version_repo = repository.SqlalchemyPostVersionRepository(session)

        for post in await post_repo.get_all():
            try:
                await post_version_repo.get_by_id(post_id=post.id, version_id=1)
            except exceptions.DoesNotExist:
                logging.info("'%s' initialized with version 1.", post.title)
                await post_version_repo.create(
                    username=post.created_by,
                    post_id=post.id,
                    post=schemas.PostInputSchema(title=post.title, text=post.text),
                )
            else:
                logging.debug("'%s' post already initialized.", post.title)
