from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from poaster.access.tables import User
from poaster.bulletin.tables import Post
from poaster.core.config import settings
from poaster.core.tables import Base

# Need to import all tables that should be autodetected by migration tool.
__all__ = [
    "Base",
    "Post",
    "User",
]

# User defined options
config = context.config
config.set_main_option("sqlalchemy.url", settings.uri)
target_metadata = Base.metadata

assert config.config_file_name is not None, "Cannot load file config without file name."

fileConfig(config.config_file_name)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section)

    assert configuration is not None, "Cannot create engine without config"

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
