from typing import Optional

import beaupy
import rich
from launchflow.config import config
from rich.progress import Progress, SpinnerColumn, TextColumn

from launchflow.clients import get_launchflow_client_legacy


def get_account_id_from_config(account_id: Optional[str]) -> str:
    if account_id is None:
        account_id = config.settings.default_account_id
    if account_id is None:
        account_id = get_account_id_no_config(account_id)
    return account_id


def get_account_id_no_config(account_id: Optional[str]) -> str:
    if account_id is None:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
        ) as progress:
            task = progress.add_task("Fetching accounts...", total=None)
            accounts = get_launchflow_client_legacy().accounts.list()
            progress.remove_task(task)
        account_ids = [f"{a.id}" for a in accounts]
        selected_account = beaupy.select(account_ids, return_index=True, strict=True)
        account_id = account_ids[selected_account]
        rich.print(f"[pink1]>[/pink1] {account_id}")
    return account_id
