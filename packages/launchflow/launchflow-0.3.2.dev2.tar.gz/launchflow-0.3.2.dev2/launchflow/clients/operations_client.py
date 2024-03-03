import time

import httpx
from launchflow.clients.response_schemas import OperationResponse, OperationStatus
from launchflow.config import config
from launchflow.exceptions import LaunchFlowRequestFailure


class OperationsClient:
    def __init__(self, http_client: httpx.Client):
        self.http_client = http_client

    def base_url(self) -> str:
        return f"{config.settings.launch_service_address}/operations"

    def stream_operation_status(self, operation_id: str):
        operation_status = OperationStatus.UNKNOWN

        while True:
            operation = self.get(operation_id)
            operation_status = operation.status

            if operation.status.is_final():
                break

            yield operation_status

            time.sleep(1)

        yield operation_status

    def get_operation_status(self, operation_id: str):
        operation = self.get(operation_id)
        return operation.status

    def get(self, operation_id: str):
        response = self.http_client.get(
            f"{self.base_url()}/{operation_id}",
            headers={"Authorization": f"Bearer {config.get_access_token()}"},
        )
        if response.status_code != 200:
            raise LaunchFlowRequestFailure(response)
        return OperationResponse.model_validate(response.json())


class OperationsAsyncClient:
    def __init__(self, http_client: httpx.AsyncClient):
        self.http_client = http_client

    def base_url(self) -> str:
        return f"{config.settings.launch_service_address}/operations"

    async def stream_operation_status(self, operation_id: str):
        operation_status = OperationStatus.UNKNOWN

        while True:
            operation = await self.get(operation_id)
            operation_status = operation.status

            if operation.status.is_final():
                break

            yield operation_status

            time.sleep(1)

        yield operation_status

    async def get_operation_status(self, operation_id: str):
        operation = await self.get(operation_id)
        return operation.status

    async def get(self, operation_id: str):
        response = await self.http_client.get(
            f"{self.base_url()}/{operation_id}",
            headers={"Authorization": f"Bearer {config.get_access_token()}"},
        )
        if response.status_code != 200:
            raise LaunchFlowRequestFailure(response)
        return OperationResponse.model_validate(response.json())
