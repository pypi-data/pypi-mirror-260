import typer
from launchflow.cli.utils import print_response
from launchflow.config import config
from launchflow.flows.project_flows import create_project

from launchflow.clients import get_launchflow_client_legacy

app = typer.Typer(help="Interact with your LaunchFlow projects.")


@app.command()
def list():
    """Lists all current projects in your account."""
    projects = get_launchflow_client_legacy().projects.list(
        config.settings.default_account_id
    )

    print_response(
        "Projects", {"projects": [projects.model_dump() for projects in projects]}
    )


@app.command()
def get(project_name: str):
    """Get information about a specific project."""
    project = get_launchflow_client_legacy().projects.get(project_name)

    print_response("Project", project.model_dump())


@app.command()
def create(
    project_name: str = typer.Argument(None, help="The name of the project to create."),
    account_id: str = typer.Option(
        None,
        help="The account ID to fetch. Of the format `acount_123`. Defaults to the account in your config file.",  # noqa: E501
    ),
):
    """Create a new project in your account."""
    project = create_project(project_name=project_name, account_id=account_id)

    print_response("Project", project.model_dump())
