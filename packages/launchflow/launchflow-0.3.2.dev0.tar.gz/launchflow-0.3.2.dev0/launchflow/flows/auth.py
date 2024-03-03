import base64
import secrets
import time
import webbrowser

import requests
import rich
from launchflow.config import config
from rich.progress import Progress, SpinnerColumn, TextColumn

from launchflow.clients import get_launchflow_client_legacy


def _generate_state(length=64):
    random_bytes = secrets.token_bytes(length)
    code_verifier = base64.urlsafe_b64encode(random_bytes).decode("utf-8")
    code_verifier = code_verifier.rstrip("=")
    return code_verifier


def login_flow():
    state = _generate_state()
    response = requests.get(
        f"{config.settings.account_service_address}/auth/login?state={state}"
    )
    if response.status_code == 200:
        authorize_url = response.json()["url"]
    else:
        raise RuntimeError(f"Failed to get auth url. {response.reason}")

    successful = webbrowser.open(authorize_url)
    if not successful:
        raise RuntimeError("Failed to open browser")

    # poll the server for the access token
    # NOTE: we print a new line to make the console output more balanced.
    print()
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    ) as progress:
        task = progress.add_task("Waiting for access token...", total=None)

        credentials = None
        while credentials is None:
            response = requests.get(
                f"{config.settings.account_service_address}/auth/access_token?state={state}"
            )
            if response.status_code == 200:
                credentials = response.json()
            elif response.status_code != 202:  # 202 = still waiting
                raise RuntimeError(f"Failed to get access token. {response.reason}")
            else:
                time.sleep(1)

        config.update_credentials(credentials)
        accounts = get_launchflow_client_legacy().accounts.list()

        if config.settings.default_account_id is None:
            # TODO: prompt user to select account
            if len(accounts) == 1:
                config.settings.default_account_id = accounts[0].id
                config.save()
            else:
                # TODO: prompt the user to select an account as their default
                pass
        progress.remove_task(task)
        progress.console.print("[green]✓[/green] Login successful")


def logout_flow():
    if config.credentials is None:
        print("Not logged in")
        return

    response = requests.post(
        f"{config.settings.account_service_address}/auth/logout",
        json={"refresh_token": config.credentials.refresh_token},
    )
    if response.status_code != 200:
        raise RuntimeError(f"Failed to logout. {response.reason}")

    config.clear_credentials()
    rich.print("[green]✓[/green] Logout successful")


def refresh_credentials_flow():
    if config.credentials is None:
        print("Not logged in")
        return

    response = requests.post(
        f"{config.settings.account_service_address}/auth/refresh",
        json={"refresh_token": config.credentials.refresh_token},
    )
    if response.status_code != 200:
        raise RuntimeError(f"Failed to refresh credentials. {response.reason}")

    config.update_credentials(response.json())
    rich.print("[green]✓[/green] Credentials refreshed")


def me_flow():
    if config.credentials is None:
        print("Not logged in")
        return

    response = requests.get(
        f"{config.settings.account_service_address}/auth/me",
        headers={"Authorization": f"Bearer {config.get_access_token()}"},
    )
    if response.status_code != 200:
        raise RuntimeError(f"Failed to get user info. {response.reason}")

    rich.print(response.json())
