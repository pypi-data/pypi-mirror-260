from pathlib import Path

from alembic import command, config

from poaster.core import sessions


def upgrade_to_head() -> None:
    """Upgrade database to head from within the app."""
    alembic_cfg_path = Path(__file__).parent / "alembic.ini"
    alembic_cfg = config.Config(alembic_cfg_path)

    with sessions.engine.begin() as connection:
        alembic_cfg.attributes["connection"] = connection
        command.upgrade(alembic_cfg, "head")
