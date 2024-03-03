import time
import webbrowser
from enum import Enum
from typing import Optional

import beaupy
import rich
from launchflow.exceptions import LaunchFlowRequestFailure
from launchflow.flows.account_id import get_account_id_from_config
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt

from launchflow.clients import get_launchflow_client_legacy


class CloudProvider(Enum):
    GCP = "GCP"
    AWS = "AWS"
    AZURE = "Azure"


CLOUD_PROVIDER_CHOICES = [
    (CloudProvider.GCP, "Google Cloud Platform"),
    (CloudProvider.AWS, "Amazon Web Services"),
    # (CloudProvider.AZURE, "Microsoft Azure"),
]


def select_cloud_provider() -> CloudProvider:
    options = [f"{f[0].value} - {f[1]}" for f in CLOUD_PROVIDER_CHOICES]
    answer = beaupy.select(options=options, return_index=True)
    rich.print(f"[pink1]>[/pink1] {options[answer]}")
    return CLOUD_PROVIDER_CHOICES[answer][0]


def connect(account_id: Optional[str], provider: Optional[CloudProvider]):
    account_id = get_account_id_from_config(account_id)
    if provider is None:
        print(
            f"\nSelect the cloud provider you would like to configure for your account ({account_id}):"
        )
        provider = select_cloud_provider()

    setup_status = get_launchflow_client_legacy().connect.status(
        account_id=account_id, include_aws_template_url=True
    )
    if provider == CloudProvider.GCP:
        _connect_gcp(
            account_id,
            setup_status.gcp_connection_info.admin_service_account_email,
        )
    elif provider == CloudProvider.AWS:
        _connect_aws(
            account_id,
            setup_status.aws_connection_info.external_role_id,
            setup_status.aws_connection_info.cloud_foundation_template_url,
        )
    else:
        raise ValueError(f"LaunchFlow currently does not support `{provider.value}`")


AWS_REGIONS = [
    "us-east-1",
    "us-east-2",
    "us-west-1",
    "us-west-2",
    "af-south-1",
    "ap-east-1",
    "ap-south-2",
    "ap-southest-3",
    "ap-southeast-4",
    "ap-south-1",
    "ap-northeast-2",
    "ap-northeast-3",
    "ap-southeast-1",
    "ap-southeast-2",
    "ap-northeast-1",
    "ca-central-1",
    "ca-west-1",
    "eu-central-1",
    "eu-central-2",
    "eu-west-1",
    "eu-west-2",
    "eu-west-3",
    "eu-south-1",
    "eu-south-2",
    "eu-north-1",
    "il-central-1",
    "me-south-1",
    "me-central-1",
    "sa-east-1",
    "us-gov-east-1",
    "us-gov-west-1",
]

_AWS_URL = "https://{region}.console.aws.amazon.com/cloudformation/home?region={region}#/stacks/create/review?stackName=LaunchFlowRole&param_LaunchFlowExternalID={external_id}&templateURL={template_url}"


def _connect_aws(account_id: str, external_role_id: str, template_url: str):
    aws_account_id = Prompt.ask(
        "\nEnter your AWS account ID (can be found in the top right corner of https://console.aws.amazon.com/). You will then be prompted to login to your AWS account"
    )
    webbrowser.open("https://console.aws.amazon.com/")

    print("\nSelect the AWS region you would like to setup LaunchFlow in:")
    region = beaupy.select(AWS_REGIONS, pagination=True)
    rich.print(f"[pink1]>[/pink1] {region}\n")

    url = _AWS_URL.format(
        region=region, external_id=external_role_id, template_url=template_url
    )
    webbrowser.open(url)
    rich.print(" - Visit the AWS Console to create a CloudFormation stack")
    rich.print(' - Scroll to the bottom and check the "I acknowledge..." box ')
    rich.print(
        ' - Click on "Create Stack". It may take a few minutes for the fole to be fully created.\n'
    )

    rich.print(
        "[i]This role will be used to provision AWS resources and deployments in your AWS account.[/i]\n"
    )

    _ = Prompt.ask(
        "Once the role is fully created hit enter to have us verify the setup"
    )

    # polls for a successful connection for up to 60 seconds
    start_time = time.time()
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    ) as progress:
        task = progress.add_task("Verifying AWS connection\n", total=None)

        done = False
        while not done:
            try:
                get_launchflow_client_legacy().connect.connect_aws(
                    account_id=account_id, aws_account_id=aws_account_id
                )
                done = True
            except LaunchFlowRequestFailure:
                if time.time() - start_time > 60:
                    raise TimeoutError(
                        "AWS setup verification timed out. Please try again."
                    )
            time.sleep(3)

        progress.remove_task(task)

    rich.print("\n[bold]AWS successfully connected[/bold] 🚀")


def _connect_gcp(account_id: str, service_account_email: str):
    rich.print(
        f"\nGrant `[cyan]{service_account_email}[/cyan]` the following roles on your GCP organization:"
    )
    rich.print("- Folder Creator ([i]roles/resourcemanager.folderCreator[/i])")
    rich.print(
        "- Organization Viewer ([i]roles/resourcemanager.organizationViewer[/i])"
    )
    rich.print("- Billing Account User ([i]roles/billing.user[/i])\n")

    rich.print(
        "[i]These roles will be used to create a unique GCP project for every environment in your account.[/i]\n"
    )

    _ = Prompt.ask("Hit enter once complete and we will verify your setup")

    # polls for a successful connection for up to 60 seconds
    start_time = time.time()
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    ) as progress:
        task = progress.add_task(
            "Verifying GCP connection (this may take a minute)...\n", total=None
        )

        done = False
        while not done:
            try:
                get_launchflow_client_legacy().connect.connect_gcp(
                    account_id=account_id
                )
                done = True
            except LaunchFlowRequestFailure:
                if time.time() - start_time > 60:
                    raise TimeoutError(
                        "GCP setup verification timed out. Please try again."
                    )
            time.sleep(3)

        progress.remove_task(task)

    rich.print("\n[bold]GCP successfully connected[/bold] 🚀")
