import click

from poaster.__about__ import __version__
from poaster.access.cli import init, run, users


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(version=__version__, prog_name="poaster")
def poaster() -> None:
    """Control panel for managing poaster application."""


poaster.add_command(init)
poaster.add_command(run)
poaster.add_command(users)
