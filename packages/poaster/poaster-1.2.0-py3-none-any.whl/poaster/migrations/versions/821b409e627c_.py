"""Add posts table.

Revision ID: 821b409e627c
Revises: 0b3ee652b174
Create Date: 2024-02-12 21:09:39.972955

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "821b409e627c"
down_revision = "0b3ee652b174"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("created_by", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("posts")
