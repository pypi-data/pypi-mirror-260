import requests
import typer
from launchflow.cli.utils import print_response
from launchflow.config import config
from launchflow.utils import get_failure_text

app = typer.Typer(help="Interact with your LaunchFlow account.")


@app.command()
def list():
    """List accounts that you have access to."""
    response = requests.get(
        f"{config.settings.account_service_address}/accounts",
        headers={"Authorization": f"Bearer {config.get_access_token()}"},
    )
    if response.status_code != 200:
        failure = get_failure_text(response)
        typer.echo(failure)
        raise typer.Exit(1)

    print_response("Accounts", response.json())


@app.command()
def get(
    account_id: str = typer.Argument(
        "The account ID to fetch. Of the format `acount_123`"
    ),
):
    """Get information about a specific account."""
    response = requests.get(
        f"{config.settings.account_service_address}/accounts/{account_id}",
        headers={"Authorization": f"Bearer {config.get_access_token()}"},
    )
    if response.status_code != 200:
        failure = get_failure_text(response)
        typer.echo(failure)
        raise typer.Exit(1)

    print_response("Account", response.json())
