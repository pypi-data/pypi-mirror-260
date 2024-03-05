from click.testing import CliRunner

from poaster import cli


def test_calling_poaster_without_args_launches_help(cli_runner: CliRunner):
    expected_help_text = """\
Usage: poaster [OPTIONS] COMMAND [ARGS]...

  Control panel for managing poaster application.

Options:
  --version   Show the version and exit.
  -h, --help  Show this message and exit.

Commands:
  init   Instantiate the application environment and secret key.
  run    Migrate database to latest version and launch application server.
  users  Control panel for managing users.
"""
    result = cli_runner.invoke(cli.poaster, [])

    assert result.exit_code == 0
    assert result.output == expected_help_text
