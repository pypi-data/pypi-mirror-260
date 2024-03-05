from sqlalchemy.sql import func
from sqlalchemy.sql.schema import Column, ForeignKey, UniqueConstraint
from sqlalchemy.sql.sqltypes import DateTime, Integer, String, Text

from poaster.core.tables import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    text = Column(Text(), nullable=False)
    created_by = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())


class PostVersion(Base):
    __tablename__ = "post_versions"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    text = Column(Text(), nullable=False)
    version = Column(Integer, nullable=False)
    updated_by = Column(String(255), nullable=False)
    updated_at = Column(DateTime, default=func.now())

    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))

    __table_args__ = (
        UniqueConstraint("post_id", "version", name="unique_post_version"),
    )
