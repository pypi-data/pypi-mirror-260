import io
from typing import Any, Dict

import httpx
from launchflow.clients.response_schemas import OperationResponse
from launchflow.config import config
from launchflow.exceptions import LaunchFlowRequestFailure


class ServicesClient:
    def __init__(self, http_client: httpx.Client):
        self.http_client = http_client

    def base_url(self, project_name: str, environment_name: str) -> str:
        return f"{config.settings.launch_service_address}/projects/{project_name}/environments/{environment_name}/services"

    def deploy(
        self,
        project_name: str,
        environment_name: str,
        product_name: str,
        service_name: str,
        tar_bytes: io.BytesIO,
        # TODO: add create args on client
        create_args: Dict[str, Any],
    ):
        response = self.http_client.post(
            f"{self.base_url(project_name, environment_name)}/{product_name}/{service_name}",
            files={"source_tarball": ("source.tar.gz", tar_bytes, "application/zip")},
            headers={"Authorization": f"Bearer {config.get_access_token()}"},
            # default timeout is 5 seconds, but submitting a build can take a while
            timeout=60,
        )
        if response.status_code != 201:
            raise LaunchFlowRequestFailure(response)
        return OperationResponse.model_validate(response.json())
