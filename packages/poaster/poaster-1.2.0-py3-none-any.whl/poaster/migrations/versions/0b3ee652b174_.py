"""Add users table.

Revision ID: 0b3ee652b174
Revises: 
Create Date: 2024-02-09 22:05:49.244176

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0b3ee652b174"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=255), nullable=False),
        sa.Column("password", sa.String(length=512), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )


def downgrade() -> None:
    op.drop_table("users")
