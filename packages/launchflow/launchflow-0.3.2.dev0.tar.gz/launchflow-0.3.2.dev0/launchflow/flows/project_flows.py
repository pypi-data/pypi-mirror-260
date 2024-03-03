from typing import Optional

import beaupy
import rich
from launchflow.clients.response_schemas import ProjectResponse
from launchflow.exceptions import LaunchFlowRequestFailure
from launchflow.flows.account_id import get_account_id_from_config
from launchflow.flows.cloud_provider import select_cloud_provider
from rich.progress import Progress, SpinnerColumn, TextColumn

from launchflow.clients import get_launchflow_client_legacy


def get_project(
    project_name: Optional[str], prompt_for_creation: bool = False
) -> ProjectResponse:
    if project_name is None:
        account_id = get_account_id_from_config(None)
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
        ) as progress:
            task = progress.add_task("Fetching projects...", total=None)
            projects = get_launchflow_client_legacy().projects.list(account_id)
            progress.remove_task(task)
        project_names = [f"{p.name}" for p in projects]
        if prompt_for_creation:
            project_names.append("[i yellow]Create new project[/i yellow]")
        print("Select the project to use:")
        selected_project = beaupy.select(project_names, return_index=True, strict=True)
        if prompt_for_creation and selected_project == len(project_names) - 1:
            project = create_project()
        else:
            project = projects[selected_project]
            rich.print(f"[pink1]>[/pink1] {project.name}")
        return project
    try:
        # Fetch the project to ensure it exists
        project = get_launchflow_client_legacy().projects.get(project_name)
    except LaunchFlowRequestFailure as e:
        if e.status_code == 404 and prompt_for_creation:
            answer = beaupy.confirm(
                f"Project `{project_name}` does not yet exist. Would you like to create it?"
            )
            if answer:
                # TODO: this will just use their default account. Should maybe ask them.
                # But maybe that should be in the create project flow?
                project = create_project()
            else:
                raise e
        else:
            raise e
    return project


def create_project(
    project_name: Optional[str] = None, account_id: Optional[str] = None
):
    if project_name is None:
        project_name = beaupy.prompt("Enter a project name:")
        rich.print(f"[pink1]>[/pink1] {project_name}")
    print()
    print("Select a cloud provider for your project: (Azure coming soon)")
    cloud_provider = select_cloud_provider()

    account_id = get_account_id_from_config(account_id)
    print()
    project = None
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    ) as progress:
        task = progress.add_task("Creating LaunchFlow Project...", total=None)
        try:
            project = get_launchflow_client_legacy().projects.create(
                project_name, cloud_provider.value.lower(), account_id
            )
        except Exception as e:
            progress.console.print("[red]✗[/red] Failed to create project.")
            raise e
        finally:
            progress.update(task, advance=1)
            progress.remove_task(task)
    progress.console.print("[green]✓[/green] Project created successfully.")
    return project
