import typer
from launchflow.cli.utils import print_response
from launchflow.exceptions import LaunchFlowRequestFailure
from launchflow.flows.account_id import get_account_id_from_config
from launchflow.flows.cloud_provider import CloudProvider
from launchflow.flows.cloud_provider import connect as connect_provider

from launchflow.clients import get_launchflow_client_legacy

app = typer.Typer(help="Commands for connecting LaunchFlow to your cloud")


@app.command()
def connect(
    account_id: str = typer.Argument(
        None, help="The account ID to fetch. Of the format `acount_123`"
    ),
    provider: CloudProvider = typer.Option(
        None, help="The cloud provider to setup your account with."
    ),
    status: bool = typer.Option(
        False,
        "--status",
        "-s",
        help="Only print out connection status instead of instructions for connecting.",
    ),
):
    """Connect your LaunchFlow account to a cloud provider (AWS or GCP) or retrieve connection info with the `--status / -s` flag."""
    if status:
        account_id = get_account_id_from_config(account_id)
        connection_status = get_launchflow_client_legacy().connect.status(account_id)
        to_print = connection_status.model_dump()
        del to_print["aws_connection_info"]["cloud_foundation_template_url"]
        print_response("Connection Status", to_print)
    else:
        try:
            connect_provider(account_id, provider)
        except LaunchFlowRequestFailure as e:
            e.pretty_print()
            raise typer.Exit(1)
        except Exception as e:
            typer.echo(str(e))
            raise typer.Exit(1)
