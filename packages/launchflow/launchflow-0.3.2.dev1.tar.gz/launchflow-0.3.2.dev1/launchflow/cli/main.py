import asyncio
import os
from typing import Optional

import beaupy
import rich
import typer
from launch_app.schemas.project_schemas import ProjectResponse
from launchflow.cli import project_gen
from launchflow.cli.accounts import account_commands
from launchflow.cli.cloud import cloud_commands
from launchflow.cli.config import config_commands
from launchflow.cli.contants import ENVIRONMENT_HELP, PROJECT_HELP, SERVICE_HELP
from launchflow.cli.environments import environment_commands
from launchflow.cli.project import project_commands
from launchflow.cli.resources import resource_commands
from launchflow.cli.resources_ast import find_launchflow_resources
from launchflow.cli.templates import (
    dockerfile_template,
    infra_dot_py_template,
    main_template,
)
from launchflow.cli.utils import tar_source_in_memory
from launchflow.clients.response_schemas import EnvironmentResponse
from launchflow.config import config
from launchflow.config.launchflow_yaml import LaunchFlowDotYaml
from launchflow.exceptions import LaunchFlowRequestFailure
from launchflow.flows.auth import login_flow, logout_flow
from launchflow.flows.environments_flows import get_environment
from launchflow.flows.project_flows import get_project
from launchflow.flows.resource_flows import clean as clean_resources
from launchflow.flows.resource_flows import create as create_resources
from launchflow.flows.resource_flows import import_resources

from launchflow.clients import get_launchflow_client_legacy

app = typer.Typer(help="LaunchFlow CLI.")
app.add_typer(account_commands.app, name="accounts")
app.add_typer(project_commands.app, name="projects")
app.add_typer(environment_commands.app, name="environments")
app.add_typer(cloud_commands.app, name="cloud")
app.add_typer(resource_commands.app, name="resources")
app.add_typer(config_commands.app, name="config")


_SCAN_DIRECTORY_HELP = (
    "Directory to scan for resources. Defaults to the current working directory."
)

_CWD_HELP = (
    "Directory to run automations from. Defaults to the current working directory."
)


def _get_project_info(
    project_name: Optional[str] = None, prompt_for_creation: bool = True
):
    # This check replaces the cli project arg with the configured project (if set)
    if project_name is None:
        project_name = config.project
    # Fetches the latest project info from the server
    return get_project(
        project_name=project_name, prompt_for_creation=prompt_for_creation
    )


def _get_environment_info(
    project: ProjectResponse,
    environment_name: Optional[str] = None,
    prompt_for_creation: bool = True,
):
    # This check replaces the cli env arg with the configured environment (if set)
    if environment_name is None:
        environment_name = config.environment
    # Fetches the latest environment info from the server
    return get_environment(
        project=project,
        environment_name=environment_name,
        prompt_for_creation=prompt_for_creation,
    )


def _get_service_info(
    project: ProjectResponse,
    environment: EnvironmentResponse,
    service_name: Optional[str] = None,
    prompt_for_creation: bool = True,
):
    service_configs = config.list_service_configs()
    if service_name is not None:
        for service in service_configs:
            if service.name == service_name:
                return service
        raise ValueError(f"Service `{service_name}` not found in launchflow.yaml.")
    if len(service_configs) == 1:
        return service_configs[0]
    # TODO: Add a flow to help the user update their launchflow.yaml
    # Consider using the project / env info to filter the service options
    # i.e. a gcp project should recommend cloud run service options
    raise ValueError("No services configured in launchflow.yaml.")


@app.command()
def init(
    directory: str = typer.Argument(".", help="Directory to initialize launchflow."),
    account_id: str = typer.Option(
        None,
        help="Account ID to use for this project. Defaults to the account ID set in the config.",
    ),
):
    """Initialize a new launchflow project."""
    try:
        project = project_gen.project(account_id)
        environment = get_environment(
            project=project,
            environment_name=None,
            prompt_for_creation=True,
        )
    except Exception as e:
        typer.echo(e)
        raise typer.Exit(1)

    full_directory_path = os.path.join(os.path.abspath(directory), project.name)
    while os.path.exists(full_directory_path):
        typer.echo(f"Directory `{full_directory_path}` already exists.")
        directory_name = beaupy.prompt("Enter a directory name for your project:")
        full_directory_path = os.path.join(os.path.abspath(directory), directory_name)

    framework = project_gen.framework()
    resources = project_gen.resources()
    infra = infra_dot_py_template.template(project.name, framework, resources)
    requirements = project_gen.requirements(framework, resources)
    dockerfile = dockerfile_template.template(framework)
    launchflow_dot_yaml = LaunchFlowDotYaml(project.name, environment.name)
    main = main_template.template(framework, resources)

    app_directory_path = os.path.join(full_directory_path, "app")
    os.makedirs(app_directory_path)

    # App level files
    infra_py = os.path.join(app_directory_path, "infra.py")
    main_py = os.path.join(app_directory_path, "main.py")
    # Top level files
    requirements_txt = os.path.join(full_directory_path, "requirements.txt")
    dockerfile_path = os.path.join(full_directory_path, "Dockerfile")
    launchflow_yaml_path = os.path.join(full_directory_path, "launchflow.yaml")

    with open(infra_py, "w") as f:
        f.write(infra)

    with open(main_py, "w") as f:
        f.write(main)

    with open(requirements_txt, "w") as f:
        f.write(requirements + "\n")

    with open(dockerfile_path, "w") as f:
        f.write(dockerfile)

    launchflow_dot_yaml.save_to_file(launchflow_yaml_path)

    print()
    print("Done!")
    print()
    print("To create your resources run:")
    rich.print("  $ [green]launchflow create")
    print()
    print("To build a docker image run:")
    rich.print("  $ [green]launchflow build")
    print()
    print("To deploy your app remotely run:")
    rich.print("  $ [green]launchflow deploy")
    print()
    print("To run all of the above in one command run:")
    rich.print("  $ [green]launchflow launch")


@app.command()
def create(
    resource: str = typer.Argument(
        None,
        help="Resource to create. If none we will scan the directory for resources.",
    ),
    project: Optional[str] = typer.Option(None, help=PROJECT_HELP),
    environment: Optional[str] = typer.Option(None, help=ENVIRONMENT_HELP),
    scan_directory: str = typer.Option(".", help=_SCAN_DIRECTORY_HELP),
):
    """Create any resources that are not already created."""
    try:
        project_info = _get_project_info(project)
        environment_info = _get_environment_info(project_info, environment)

        if resource is None:
            resources = find_launchflow_resources(scan_directory)
        else:
            resources = [resource]

        asyncio.run(
            create_resources(
                project_info.name, environment_info.name, *import_resources(resources)
            )
        )
    except LaunchFlowRequestFailure as e:
        e.pretty_print()
        raise typer.Exit(1)


@app.command()
def clean(
    scan_directory: str = typer.Option(".", help=_SCAN_DIRECTORY_HELP),
    project: Optional[str] = typer.Option(None, help=PROJECT_HELP),
    environment: Optional[str] = typer.Option(None, help=ENVIRONMENT_HELP),
):
    """Clean up any resources that are not in the current directory but are part of the project / environment."""
    try:
        project_info = _get_project_info(project)
        environment_info = _get_environment_info(project_info, environment)

        resources = find_launchflow_resources(scan_directory)
        asyncio.run(
            clean_resources(
                project_info.name, environment_info.name, *import_resources(resources)
            )
        )
    except LaunchFlowRequestFailure as e:
        e.pretty_print()
        raise typer.Exit(1)


@app.command(hidden=True)
def deploy(
    cwd: str = typer.Option(".", help=_CWD_HELP),
    project: Optional[str] = typer.Option(None, help=PROJECT_HELP),
    environment: Optional[str] = typer.Option(None, help=ENVIRONMENT_HELP),
    service: Optional[str] = typer.Option(None, help=SERVICE_HELP),
):
    lf_client = get_launchflow_client_legacy()

    try:
        project_info = _get_project_info(project)
        environment_info = _get_environment_info(project_info, environment)
        service_info = _get_service_info(project_info, environment_info, service)

        # TODO: move the logic below to a shared flow so we can call from cli + python

        tar_bytes = tar_source_in_memory(directory=cwd)

        operation = lf_client.services.deploy(
            project_name=project_info.name,
            environment_name=environment_info.name,
            product_name=service_info.product,
            service_name=service_info.name,
            tar_bytes=tar_bytes,
            create_args=service_info.product_config.to_dict(),
        )

        print(operation)

    except LaunchFlowRequestFailure as e:
        e.pretty_print()
        lf_client.close()
        raise typer.Exit(1)

    lf_client.close()


@app.command()
def login():
    """Login to LaunchFlow. If you haven't signup this will create a free account for you."""
    try:
        login_flow()
    except Exception as e:
        typer.echo(f"Failed to login. {e}")
        typer.Exit(1)


@app.command()
def logout():
    """Logout of LaunchFlow."""
    try:
        logout_flow()
    except Exception as e:
        typer.echo(f"Failed to logout. {e}")
        typer.Exit(1)


if __name__ == "__main__":
    app()
