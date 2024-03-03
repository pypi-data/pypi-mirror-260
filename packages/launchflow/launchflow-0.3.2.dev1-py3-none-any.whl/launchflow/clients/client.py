import httpx
from launchflow.clients.accounts_client import AccountsAsyncClient, AccountsClient
from launchflow.clients.connect_client import CloudConectAsyncClient, CloudConectClient
from launchflow.clients.environments_client import (
    EnvironmentsAsyncClient,
    EnvironmentsClient,
)
from launchflow.clients.operations_client import OperationsAsyncClient, OperationsClient
from launchflow.clients.projects_client import ProjectsAsyncClient, ProjectsClient
from launchflow.clients.resources_client import ResourcesAsyncClient, ResourcesClient
from launchflow.clients.services_client import ServicesClient


# TODO: add caching so we don't look up the same entities during a session.
class LaunchFlowClient:
    def __init__(self) -> None:
        self.http_client = httpx.Client(timeout=60)
        self.accounts = AccountsClient(self.http_client)
        self.environments = EnvironmentsClient(self.http_client)
        self.projects = ProjectsClient(self.http_client)
        self.connect = CloudConectClient(self.http_client)
        self.resources = ResourcesClient(self.http_client)
        self.services = ServicesClient(self.http_client)
        self.operations = OperationsClient(self.http_client)

    def close(self):
        self.http_client.close()


class LaunchFlowAsyncClient:
    def __init__(self) -> None:
        self.http_client = httpx.AsyncClient(timeout=60)
        self.accounts = AccountsAsyncClient(self.http_client)
        self.environments = EnvironmentsAsyncClient(self.http_client)
        self.projects = ProjectsAsyncClient(self.http_client)
        self.connect = CloudConectAsyncClient(self.http_client)
        self.resources = ResourcesAsyncClient(self.http_client)
        self.operations = OperationsAsyncClient(self.http_client)

    async def close(self):
        await self.http_client.aclose()
