from typing import Optional

import typer
from launchflow.cli.utils import print_response
from launchflow.clients.response_schemas import EnvironmentType
from launchflow.flows.environments_flows import create_environment
from launchflow.flows.project_flows import get_project

from launchflow.clients import get_launchflow_client_legacy

app = typer.Typer(help="Interact with your LaunchFlow environments.")


@app.command()
def create(
    name: str = typer.Argument(None, help="The environment name."),
    project: str = typer.Option(
        None, help="The project to create the environments in."
    ),
    env_type: Optional[EnvironmentType] = typer.Option(
        None, help="The environment type (`development` or `production`)."
    ),
):
    """Create a new environment in a LaunchFlow project."""
    try:
        project = get_project(project)
        environment = create_environment(name, project, env_type)
    except Exception as e:
        typer.echo(e)
        raise typer.Exit(1)

    print_response("Environment", environment.model_dump())


@app.command()
def list(
    project: str = typer.Option(None, help="The project to list environments for.")
):
    """List all environments in a LaunchFlow project."""
    try:
        project = get_project(project)
        environments = get_launchflow_client_legacy().environments.list(project.name)
    except Exception as e:
        typer.echo(e)
        raise typer.Exit(1)

    print_response(
        "Environments",
        {"environments": [env.model_dump(mode="json") for env in environments]},
    )


@app.command()
def get(
    name: str = typer.Argument(..., help="The environment name."),
    project: str = typer.Option(None, help="The project the environment is in."),
):
    """Get information about a specific environment."""
    try:
        project = get_project(project)
        environment = get_launchflow_client_legacy().environments.get(
            project.name, name
        )
    except Exception as e:
        typer.echo(e)
        raise typer.Exit(1)

    print_response("Environment", environment.model_dump())
