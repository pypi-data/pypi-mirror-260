import asyncio
import os

import click
import pydantic
import uvicorn
import uvicorn.config

from poaster.core import config, exceptions, hashing, sessions
from poaster.migrations.upgrade import upgrade_to_head

from . import repository, services


@click.command()
def init() -> None:
    """Instantiate the application environment and secret key."""
    click.secho("Secret key for application:", fg="green")

    if os.environ.get("SECRET_KEY"):
        click.echo("Key already found in your environment: `SECRET_KEY`\n")
    else:
        click.echo(f"SECRET_KEY={hashing.generate_secret_token()}")
        click.secho("Copy and paste this into your `.env` file.\n", fg="yellow")

    click.secho("Migrating database to head:", fg="green")
    upgrade_to_head()
    click.echo("Successfully migrated to head.")


@click.command()
@click.option(
    "--host",
    type=str,
    default="127.0.0.1",
    help="Bind socket to this host.",
    show_default=True,
)
@click.option(
    "--port",
    type=int,
    default=8000,
    help="Bind socket to this port.",
    show_default=True,
)
def run(host: str, port: int) -> None:
    """Migrate database to latest version and launch application server."""

    click.secho("Migrating database to head:", fg="green")
    upgrade_to_head()
    click.echo("Successfully migrated to head.\n")

    click.secho("Starting server...", fg="green")
    uvicorn.run(
        "poaster.app:app",
        host=host,
        port=port,
        log_level=config.settings.log_level,
    )


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def users() -> None:
    """Control panel for managing users."""


@click.command("add")
@click.option(
    "--username",
    type=str,
    prompt="Username",
    help="Username input. [prompt]",
)
@click.option(
    "--password",
    type=str,
    prompt="Password",
    hide_input=True,
    confirmation_prompt=True,
    help="Password input. [prompt]",
)
def add_user(username: str, password: str) -> None:
    """Add new user."""
    try:
        asyncio.run(add_user_(username, password))
    except exceptions.AlreadyExists:
        click.secho("User already exists.", fg="yellow")
    except pydantic.ValidationError as err:
        click.secho(f"Input validation failed: {err}", fg="yellow")
    else:
        click.secho(f"`{username}` successfully added.", fg="green")


async def add_user_(username: str, password: str) -> None:
    async with sessions.async_session() as session:
        user_repository = repository.SqlalchemyUserRepository(session)
        await services.register_user(user_repository, username, password)
        await session.commit()


@click.command("list")
def list_usernames() -> None:
    """List stored usernames."""
    if usernames := asyncio.run(list_usernames_()):
        click.secho("Stored users:", fg="green")
        for username in sorted(usernames):
            click.echo(f"- {username}")
    else:
        click.secho("No users found.", fg="yellow")


async def list_usernames_() -> list[str]:
    async with sessions.async_session() as session:
        user_repository = repository.SqlalchemyUserRepository(session)
        return await services.list_usernames(user_repository)


users.add_command(add_user)
users.add_command(list_usernames)
