import httpx
from launchflow.clients.response_schemas import ProjectResponse
from launchflow.config import config
from launchflow.exceptions import LaunchFlowRequestFailure


class ProjectsClient:
    def __init__(self, http_client: httpx.Client):
        self.http_client = http_client
        self.url = f"{config.settings.launch_service_address}/projects"

    def create(self, project_name: str, cloud_provider: str, account_id: str):
        body = {
            "name": project_name,
            "cloud_provider": cloud_provider,
        }
        response = self.http_client.post(
            f"{self.url}/{cloud_provider.lower()}?account_id={account_id}",
            json=body,
            headers={"Authorization": f"Bearer {config.get_access_token()}"},
        )
        if response.status_code != 200:
            raise LaunchFlowRequestFailure(response)
        return ProjectResponse.model_validate(response.json())

    def get(self, project_name: str):
        response = self.http_client.get(
            f"{self.url}/{project_name}",
            headers={"Authorization": f"Bearer {config.get_access_token()}"},
        )
        if response.status_code != 200:
            raise LaunchFlowRequestFailure(response)
        return ProjectResponse.model_validate(response.json())

    def list(self, account_id: str):
        response = self.http_client.get(
            f"{self.url}?account_id={account_id}",
            headers={"Authorization": f"Bearer {config.get_access_token()}"},
        )
        if response.status_code != 200:
            raise LaunchFlowRequestFailure(response)
        return [
            ProjectResponse.model_validate(project)
            for project in response.json()["projects"]
        ]


class ProjectsAsyncClient:
    def __init__(self, http_client: httpx.AsyncClient):
        self.http_client = http_client
        self.url = f"{config.settings.launch_service_address}/projects"

    async def create(self, project_name: str, cloud_provider: str, account_id: str):
        body = {
            "name": project_name,
            "cloud_provider": cloud_provider,
        }
        response = await self.http_client.post(
            f"{self.url}/{cloud_provider.lower()}?account_id={account_id}",
            json=body,
            headers={"Authorization": f"Bearer {config.get_access_token()}"},
        )
        if response.status_code != 200:
            raise LaunchFlowRequestFailure(response)
        return ProjectResponse.model_validate(response.json())

    async def get(self, project_name: str):
        response = await self.http_client.get(
            f"{self.url}/{project_name}",
            headers={"Authorization": f"Bearer {config.get_access_token()}"},
        )
        if response.status_code != 200:
            raise LaunchFlowRequestFailure(response)
        return ProjectResponse.model_validate(response.json())

    async def list(self, account_id: str):
        response = await self.http_client.get(
            f"{self.url}?account_id={account_id}",
            headers={"Authorization": f"Bearer {config.get_access_token()}"},
        )
        if response.status_code != 200:
            raise LaunchFlowRequestFailure(response)
        return [
            ProjectResponse.model_validate(project)
            for project in response.json()["projects"]
        ]
