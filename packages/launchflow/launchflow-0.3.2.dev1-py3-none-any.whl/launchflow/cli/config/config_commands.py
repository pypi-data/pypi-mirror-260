from typing import Optional

import typer
from launchflow.cli.utils import print_response
from launchflow.config import config
from launchflow.flows.account_id import get_account_id_no_config

app = typer.Typer(
    help="Commands for interacting with your local LaunchFlow configuration."
)


@app.command()
def get():
    """Print out the current LaunchFlow config."""
    print_response("Config", config.info())


@app.command()
def set_default_account_id(
    account_id: Optional[str] = typer.Argument(
        None,
        help="The account ID to set as the default. If not provided, you will be prompted to select one.",
    )
):
    """Set the default account ID for the LaunchFlow CLI."""
    account_id = get_account_id_no_config(account_id)
    config.settings.default_account_id = account_id
    config.save()
    print_response("Config", config.info())
