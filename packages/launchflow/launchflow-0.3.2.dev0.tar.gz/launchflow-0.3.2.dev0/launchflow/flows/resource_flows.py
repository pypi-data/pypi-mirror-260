import asyncio
import sys
from typing import List, Optional, Tuple, Union

import beaupy
import deepdiff
import rich
from launchflow.cli.utils import import_from_string
from launchflow.clients.response_schemas import OperationStatus, ResourceResponse
from launchflow.context.launchflow_ctx import AsyncNoOp, AsyncResourceOp
from launchflow.resource import Resource
from rich.progress import Progress, SpinnerColumn, TextColumn

from launchflow.clients import LaunchFlowAsyncClient, async_launchflow_client_ctx


def compare_dicts(d1, d2):
    return "\n        ".join(
        deepdiff.DeepDiff(d1, d2)
        .pretty()
        # NOTE: we replace these so rich doesn't get upset
        .replace("[", "{")
        .replace("]", "}")
        .replace("root", "")
        .split("\n")
    )


async def _print_operation_status(
    async_launchflow_client: LaunchFlowAsyncClient,
    progress: Progress,
    status: Optional[OperationStatus],
    resource: Resource,
    operation_type: str,
    project: str,
    environment: str,
):
    if status is None:
        progress.console.print(
            f"[yellow]✗[/yellow] {operation_type} status unknown for [blue]{resource}[/blue]"
        )
    elif status.is_success():
        progress.console.print(
            f"[green]✓[/green] {operation_type} successful for [blue]{resource}[/blue]"
        )
        return True
    elif status.is_error():
        remote_resource = await async_launchflow_client.resources.get(
            project_name=project,
            environment_name=environment,
            resource_name=resource.name,
        )
        progress.console.print(
            f"[red]✗[/red] {operation_type} failed for [blue]{resource}[/blue]"
        )
        if remote_resource.status_message:
            progress.console.print(f"    └── {remote_resource.status_message}")
        progress.console.print("")
    elif status.is_cancelled():
        progress.console.print(
            f"[yellow]✗[/yellow] {operation_type} cancelled for [blue]{resource}[/blue]"
        )
    else:
        progress.console.print(
            f"[yellow]?[/yellow] {operation_type} status unknown for [blue]{resource}[/blue]"
        )
    return False


async def _monitor_delete_resource_operations(
    async_launchflow_client: LaunchFlowAsyncClient,
    project: str,
    environment: str,
    resource_to_delete: List[ResourceResponse],
):
    # Add a new line here to make output a little cleaner
    print()
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    ) as progress:
        operations = []
        task_to_resource = {}
        for resource in resource_to_delete:
            task = progress.add_task(f"Deleting [blue]{resource}[/blue]...", total=1)
            task_to_resource[task] = resource
            name = resource.name.split("/")[-1]
            operations.append(
                (
                    await async_launchflow_client.resources.delete(
                        project_name=project,
                        environment_name=environment,
                        resource_name=name,
                    ),
                    task,
                )
            )
        successes = 0
        failures = 0
        while operations:
            await asyncio.sleep(3)
            to_stream_operations = []
            for operation, task in operations:
                status = await async_launchflow_client.operations.get_operation_status(
                    operation_id=operation.id
                )
                if status.is_final():
                    progress.remove_task(task)
                    resource = task_to_resource[task]
                    success = await _print_operation_status(
                        async_launchflow_client=async_launchflow_client,
                        progress=progress,
                        status=status,
                        resource=resource,
                        operation_type="Deletion",
                        project=project,
                        environment=environment,
                    )
                    if success:
                        successes += 1
                    else:
                        failures += 1
                else:
                    to_stream_operations.append((operation, task))
            operations = to_stream_operations
        if successes:
            progress.console.print(
                f"[green]✓[/green] Successfully deleted {successes} resources"
            )
        if failures:
            progress.console.print(
                f"[red]✗[/red] Failed to delete {failures} resources"
            )


async def _print_operation_status_v2(
    progress: Progress,
    status: Optional[OperationStatus],
    resource_ref: str,
    operation_type: str,
):
    if status is None:
        progress.console.print(
            f"[yellow]✗[/yellow] {operation_type} status unknown for [blue]{resource_ref}[/blue]"
        )
    elif status.is_success():
        progress.console.print(
            f"[green]✓[/green] {operation_type} successful for [blue]{resource_ref}[/blue]"
        )
        return True
    elif status.is_error():
        progress.console.print(
            f"[red]✗[/red] {operation_type} failed for [blue]{resource_ref}[/blue]"
        )
        # TODO: Add status message to the Operation wrapper so we can print it here
        # if remote_resource.status_message:
        #     progress.console.print(f"    └── {remote_resource.status_message}")
        progress.console.print("")
    elif status.is_cancelled():
        progress.console.print(
            f"[yellow]✗[/yellow] {operation_type} cancelled for [blue]{resource_ref}[/blue]"
        )
    else:
        progress.console.print(
            f"[yellow]?[/yellow] {operation_type} status unknown for [blue]{resource_ref}[/blue]"
        )
    return False


async def _run_and_monitor_resource_operations(resource_ops: List[AsyncResourceOp]):
    # Add a new line here to make output a little cleaner
    print()
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    ) as progress:
        operations: List[Tuple[AsyncResourceOp, int]] = []
        for resource_op in resource_ops:
            if resource_op._type == "create":
                op_type = "Creating"
            elif resource_op._type == "replace":
                op_type = "Replacing"
            else:
                raise ValueError(f"Unknown operation type {resource_op._type}")
            task = progress.add_task(
                f"{op_type} [blue]{resource_op.resource_ref}[/blue]...", total=1
            )
            operations.append((resource_op, task))

        # NOTE: This is what actually starts the operations
        await asyncio.gather(*[op.run() for op in resource_ops])

        create_successes = 0
        create_failures = 0
        replace_successes = 0
        replace_failures = 0
        while operations:
            await asyncio.sleep(3)
            to_stream_operations = []
            for operation, task in operations:
                status = await operation.get_status()
                if status.is_final():
                    progress.remove_task(task)
                    success = await _print_operation_status_v2(
                        progress=progress,
                        status=status,
                        resource_ref=operation.resource_ref,
                        operation_type=(
                            "Creation" if operation._type == "create" else "Replacement"
                        ),
                    )
                    if success:
                        if operation._type == "replace":
                            replace_successes += 1
                        else:
                            create_successes += 1
                    else:
                        if operation._type == "replace":
                            replace_failures += 1
                        else:
                            create_failures += 1
                else:
                    to_stream_operations.append((operation, task))
            operations = to_stream_operations
        if create_successes:
            progress.console.print(
                f"[green]✓[/green] Successfully created {create_successes} resources"
            )
        if replace_successes:
            progress.console.print(
                f"[green]✓[/green] Successfully replaced {replace_successes} resources"
            )
        if create_failures:
            progress.console.print(
                f"[red]✗[/red] Failed to create {create_failures} resources"
            )
        if replace_failures:
            progress.console.print(
                f"[red]✗[/red] Failed to replace {replace_failures} resources"
            )


def import_resources(resource_import_strs: List[str]) -> List[Resource]:
    sys.path.insert(0, "")
    resources: List[Resource] = []
    for resource_str in resource_import_strs:
        imported_resource = import_from_string(resource_str)
        if not isinstance(imported_resource, Resource):
            raise ValueError(f"Resource {resource_str} is not a valid Resource")
        resources.append(imported_resource)
    return resources


async def create(
    project: str, environment: str, *resources: Resource, prompt: bool = True
):
    # 1. Check which resources exist and whicn don't
    # TODO: do this async or maybe add a batch get endpoint
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    ) as progress:
        task = progress.add_task(
            f"Loading application for: [bold yellow]`{project}/{environment}`[/bold yellow]",
        )
        all_resource_ops = []

        for resource in resources:
            all_resource_ops.append(
                resource.create_async(
                    replace=True, project_name=project, environment_name=environment
                )
            )

        all_resource_ops: List[
            Union[AsyncResourceOp, AsyncNoOp]
        ] = await asyncio.gather(*all_resource_ops)

        create_ops: List[AsyncResourceOp] = []
        replace_ops: List[AsyncResourceOp] = []
        no_ops: List[AsyncNoOp] = []
        for op in all_resource_ops:
            if op._type == "create":
                create_ops.append(op)
            elif op._type == "replace":
                replace_ops.append(op)
            elif op._type == "noop":
                no_ops.append(op)
                progress.console.print(
                    f"[green]✓[/green] [blue]{op.resource_ref}[/blue] already exists"
                )
            else:
                raise ValueError(f"Unknown operation type {op._type}")

        progress.remove_task(task)

    # 2. Prompt the user for what should be created
    to_run = []
    if not create_ops and not replace_ops:
        progress.console.print(
            "[green]✓[/green] All resources already exist. No action required."
        )
        return
    if prompt:
        options = []
        all_resources = []
        for op in create_ops:
            options.append(f"[bold]Create[/bold]: [blue]{op.resource_ref}[/blue]")
            all_resources.append((op, False))
        for op in replace_ops:
            options.append(
                f"[bold]Replace[/bold]: [blue]{op}[/blue]\n"
                f"    └── {compare_dicts(op._create_args, op._replace_args)}"
            )
            all_resources.append((op, True))
        rich.print(
            f"Select the resource operations you would like to perform in [bold yellow]`{project}/{environment}`[/bold yellow]:"
        )
        answers = beaupy.select_multiple(
            options, return_indices=True, ticked_indices=list(range(len(options)))
        )
        for answer in answers:
            op, replace = all_resources[answer]
            rich.print(f"[pink1]>[/pink1] {options[answer]}")
            to_run.append(op)
        if not to_run:
            progress.console.print(
                "[green]✓[/green] No resources selected. No action required."
            )
            return
    else:
        for op in create_ops:
            to_run.append(op)
        for op in replace_ops:
            to_run.append(op)

    # 3. Create the resources
    await _run_and_monitor_resource_operations(to_run)


async def clean(
    project: str,
    environment: str,
    *local_resources: Resource,
    prompt: bool = True,
):
    async with async_launchflow_client_ctx() as async_launchflow_client:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
        ) as progress:
            task = progress.add_task(
                f"Loading application for: [bold yellow]`{project}/{environment}`[/bold yellow]",
            )
            keyed_local_resources = {}
            for local_resource in local_resources:
                name = f"{project}/{environment}/{local_resource.name}"
                keyed_local_resources[name] = local_resource
            remote_resources = await async_launchflow_client.resources.list(
                project_name=project,
                environment_name=environment,
            )

            to_delete_options = []
            for remote_resource in remote_resources:
                if (
                    remote_resource.name not in keyed_local_resources
                    and remote_resource.status in ["ready", "failed"]
                ):
                    to_delete_options.append(remote_resource)
            progress.remove_task(task)
        to_delete = []
        if not to_delete_options:
            progress.console.print(
                "[green]✓[/green] No resources to delete. No action required."
            )
            return
        if prompt:
            rich.print(
                f"The following resources were unused in [bold yellow]`{project}/{environment}`[/bold yellow]. Select the resources you would like to [bold]delete[/bold]:"
            )
            options = [
                f"[bold]Delete[/bold]: [bold]{str(resource)}[/bold]"
                for resource in to_delete_options
            ]
            answers = beaupy.select_multiple(options, return_indices=True)
            for answer in answers:
                rich.print(
                    f"[pink1]>[/pink1] Delete: [blue]{to_delete_options[answer]}[/blue]"
                )
                to_delete.append(to_delete_options[answer])
            if not to_delete:
                rich.print(
                    "[green]✓[/green] No resources selected. No action required."
                )
                return
        else:
            to_delete = to_delete_options
        await _monitor_delete_resource_operations(
            async_launchflow_client, project, environment, to_delete
        )
