import typer
from launchflow.cli.contants import ENVIRONMENT_HELP, PROJECT_HELP
from launchflow.cli.utils import print_response
from launchflow.exceptions import LaunchFlowRequestFailure
from launchflow.flows.environments_flows import get_environment
from launchflow.flows.project_flows import get_project

from launchflow.clients import get_launchflow_client_legacy

app = typer.Typer(help="Commands for managing resources in LaunchFlow")


@app.command()
def get(
    resource_name: str = typer.Argument(..., help="Resource to ping."),
    project: str = typer.Option(None, help=PROJECT_HELP),
    environment: str = typer.Option(None, help=ENVIRONMENT_HELP),
):
    """Fetch information about a resource."""
    project = get_project(project, prompt_for_creation=False)
    environment = get_environment(
        project=project, environment_name=environment, prompt_for_creation=False
    )
    try:
        resource = get_launchflow_client_legacy().resources.get(
            project.name, environment.name, resource_name
        )

        print_response("Resource", resource.model_dump())
    except LaunchFlowRequestFailure as e:
        e.pretty_print()
        raise typer.Exit(1)


@app.command()
def list(
    project: str = typer.Option(None, help=PROJECT_HELP),
    environment: str = typer.Option(None, help=ENVIRONMENT_HELP),
):
    """List all resources in a project/environment."""
    try:
        project = get_project(project, prompt_for_creation=False)
        environment = get_environment(
            project=project,
            environment_name=environment,
            prompt_for_creation=False,
        )
        resources = get_launchflow_client_legacy().resources.list(
            project.name, environment.name
        )
        print_response(
            "Resources",
            {
                "resources": [r.model_dump() for r in resources],
            },
        )
    except LaunchFlowRequestFailure as e:
        e.pretty_print()
        raise typer.Exit(1)
