import logging
import os
from dataclasses import dataclass
from typing import Callable, Coroutine, Dict, Literal, Optional

import fsspec
import yaml
from launchflow.cache import cache
from launchflow.clients.response_schemas import OperationResponse, OperationStatus
from launchflow.config import config

from launchflow import exceptions
from launchflow.clients import LaunchFlowAsyncClient, LaunchFlowClient


def maybe_clear_resource_cache(
    project_name: str,
    environment_name: str,
    product_name: str,
    resource_name: str,
):
    try:
        cache.delete_resource_connection_info(
            project_name, environment_name, product_name, resource_name
        )
        cache.delete_resource_connection_bucket_path(
            project_name, environment_name, product_name, resource_name
        )
    except Exception as e:
        logging.warning(f"Failed to delete resource connection info from cache: {e}")
        pass


def build_resource_uri(
    project_name: str, environment_name: str, product_name: str, resource_name: str
) -> str:
    return f"{project_name}/{environment_name}/{product_name}/{resource_name}"


# NOTE: This is either a create or replace operation. Should we split into two classes?
@dataclass
class ResourceOp:
    resource_ref: str
    operation_id: Optional[str]
    client: LaunchFlowClient
    _op: Callable[[], OperationResponse]
    _type: Literal["create", "replace"]
    _create_args: Optional[Dict] = None
    _replace_args: Optional[Dict] = None

    def run(self):
        if self.operation_id is not None:
            raise exceptions.OperationAlreadyStarted(str(self))

        operation = self._op()
        self.operation_id = operation.id

    def stream_status(self):
        if self.operation_id is None:
            raise exceptions.OperationNotStarted(str(self))
        for status in self.client.operations.stream_operation_status(self.operation_id):
            yield status

    def get_status(self):
        if self.operation_id is None:
            raise exceptions.OperationNotStarted(str(self))
        return self.client.operations.get_operation_status(self.operation_id)

    def done(self):
        return self.get_status().is_final()

    def result(self):
        # starts and blocks until the operation is done
        self.run()
        for status in self.stream_status():
            if status.is_final():
                return status


@dataclass
class AsyncResourceOp:
    resource_ref: str
    operation_id: Optional[str]
    client: LaunchFlowAsyncClient
    _op: Callable[[], Coroutine[None, None, OperationResponse]]
    _type: Literal["create", "replace"]
    _create_args: Optional[Dict] = None
    _replace_args: Optional[Dict] = None

    async def run(self):
        if self.operation_id is not None:
            raise exceptions.OperationAlreadyStarted(str(self))

        operation = await self._op()
        self.operation_id = operation.id

    async def stream_status(self):
        if self.operation_id is None:
            raise exceptions.OperationNotStarted(str(self))
        async for status in self.client.operations.stream_operation_status(
            self.operation_id
        ):
            yield status

    async def get_status(self):
        if self.operation_id is None:
            raise exceptions.OperationNotStarted(str(self))
        return await self.client.operations.get_operation_status(self.operation_id)

    async def done(self):
        return (await self.get_status()).is_final()

    async def result(self):
        # starts and blocks until the operation is done
        self.run()
        async for status in self.stream_status():
            if status.is_final():
                return status


@dataclass
class NoOp:
    resource_ref: str
    _type: Literal["noop"] = "noop"

    def run(self):
        pass

    def stream_status(self):
        yield OperationStatus.SUCCESS

    def get_status(self):
        return OperationStatus.SUCCESS

    def done(self):
        return True

    def result(self):
        return OperationStatus.SUCCESS


@dataclass
class AsyncNoOp:
    resource_ref: str
    _type: Literal["noop"] = "noop"

    async def run(self):
        pass

    async def stream_status(self):
        yield OperationStatus.SUCCESS

    async def get_status(self):
        return OperationStatus.SUCCESS

    async def done(self):
        return True

    async def result(self):
        return OperationStatus.SUCCESS


# NOTE: This class is currently only used by the Resource class. The CLI flows have
# their own version of this module since the logic is a bit different.
@dataclass
class LaunchFlowContext:
    client: LaunchFlowClient = LaunchFlowClient()

    def get_resource_connection_info(
        self,
        product_name: str,
        resource_name: str,
        project_name: Optional[str] = None,
        environment_name: Optional[str] = None,
    ) -> Dict:
        # Step 0: Resolve the project and environment names if not provided
        project_name = project_name or config.project
        environment_name = environment_name or config.environment
        if project_name is None or environment_name is None:
            raise exceptions.ProjectOrEnvironmentNotSet(project_name, environment_name)

        resource_uri = build_resource_uri(
            project_name, environment_name, product_name, resource_name
        )

        # Step 1: Check if the connection info should be fetched from a mounted volume
        if config.env.connection_path is not None:
            local_resource_path = os.path.join(
                config.env.connection_path, resource_name, "latest"
            )
            if not os.path.exists(local_resource_path):
                logging.warning(
                    f"Connection info for resource '{resource_uri}' not found on disk."
                )
            else:
                with open(local_resource_path) as f:
                    return yaml.load(f, Loader=yaml.FullLoader)

        # Step 2: Check the cache for connection info, otherwise fetch from remote
        resource_connection_info = cache.get_resource_connection_info(
            project_name, environment_name, product_name, resource_name
        )
        if resource_connection_info is not None:
            logging.debug(f"Using cached resource connection info for {resource_uri}")
            return resource_connection_info

        # Step 3: Check if the connection bucket is set as an environment variable
        if config.env.connection_bucket is not None:
            # If the bucket env var is set, we use it to build the connection path
            connection_bucket_path = (
                f"gs://{config.env.connection_bucket}/resources/{resource_name}.yaml"
            )
            logging.debug(
                "Using connection bucket path built from environment variable for {resource_uri}"
            )
        else:
            # If the bucket env var is not set, we check the cache or fetch from remote
            connection_bucket_path = cache.get_resource_connection_bucket_path(
                project_name, environment_name, product_name, resource_name
            )
            if connection_bucket_path is None:
                logging.debug(
                    f"Fetching bucket connection info from remote server for {resource_uri}"
                )
                resource_info = self.client.resources.get(
                    project_name=project_name,
                    environment_name=environment_name,
                    resource_name=resource_name,
                    product_name_to_validate=product_name,
                )
                if resource_info.connection_bucket_path is None:
                    raise exceptions.RemoteConnectionInfoMissing(resource_info)
                connection_bucket_path = resource_info.connection_bucket_path
                cache.set_resource_connection_bucket_path(
                    project_name,
                    environment_name,
                    product_name,
                    resource_name,
                    connection_bucket_path,
                )
            else:
                logging.debug(f"Using cached bucket connection info for {resource_uri}")

        # Step 4: Fetch the resource connection info from the connection storage bucket
        try:
            with fsspec.open(connection_bucket_path, mode="r") as file:
                resource_connection_info = yaml.safe_load(file.read())
        except FileNotFoundError:
            raise exceptions.ConnectionInfoNotFound(resource_name)

        # Step 5: Cache the resource connection info
        cache.set_resource_connection_info(
            project_name,
            environment_name,
            product_name,
            resource_name,
            resource_connection_info,
        )

        # Step 6: Return the resource connection info
        return resource_connection_info

    def create_resource_operation(
        self,
        product_name: str,
        resource_name: str,
        create_args: Dict,
        project_name: Optional[str] = None,
        environment_name: Optional[str] = None,
        replace: bool = False,
    ):
        project_name = project_name or config.project
        environment_name = environment_name or config.environment
        if project_name is None or environment_name is None:
            raise exceptions.ProjectOrEnvironmentNotSet(project_name, environment_name)

        try:
            existing_resource = self.client.resources.get(
                project_name=project_name,
                environment_name=environment_name,
                resource_name=resource_name,
                product_name_to_validate=product_name,
            )
        except exceptions.LaunchFlowRequestFailure as e:
            if e.status_code != 404:
                raise
            existing_resource = None

        if existing_resource and existing_resource.create_args == create_args:
            logging.debug(
                f"Resource '{resource_name}' already exists with the same create args"
            )
            return NoOp(resource_ref=f"Resource(name={resource_name})")

        elif existing_resource:
            if not replace:
                raise exceptions.ResourceReplacementRequired(resource_name)

            def replace_operation():
                # NOTE: We attempt to clear the cache info when the op is applied, but
                # swallow any exceptions since its not critical to the operation
                maybe_clear_resource_cache(
                    project_name, environment_name, product_name, resource_name
                )

                return self.client.resources.replace(
                    project_name=project_name,
                    environment_name=environment_name,
                    product_name=product_name,
                    resource_name=resource_name,
                    create_args=create_args,
                )

            return ResourceOp(
                resource_ref=f"Resource(name={resource_name})",
                operation_id=None,
                client=self.client,
                _op=replace_operation,
                _type="replace",
                create_args=create_args,
                replace_args=existing_resource.create_args,
            )

        else:

            def create_operation():
                # NOTE: We attempt to clear the cache info when the op is applied, but
                # swallow any exceptions since its not critical to the operation
                maybe_clear_resource_cache(
                    project_name, environment_name, product_name, resource_name
                )
                return self.client.resources.create(
                    project_name=project_name,
                    environment_name=environment_name,
                    product_name=product_name,
                    resource_name=resource_name,
                    create_args=create_args,
                )

            return ResourceOp(
                resource_ref=f"Resource(name={resource_name})",
                operation_id=None,
                client=self.client,
                _op=create_operation,
                _type="create",
            )


# TODO: Better abstract the client and operation logic so we dont duplicate it
@dataclass
class LaunchFlowAsyncContext:
    client: LaunchFlowAsyncClient = LaunchFlowAsyncClient()

    async def get_resource_connection_info(
        self,
        product_name: str,
        resource_name: str,
        project_name: Optional[str] = None,
        environment_name: Optional[str] = None,
    ) -> Dict:
        # Step 0: Resolve the project and environment names if not provided
        project_name = project_name or config.project
        environment_name = environment_name or config.environment
        if project_name is None or environment_name is None:
            raise exceptions.ProjectOrEnvironmentNotSet(project_name, environment_name)

        resource_uri = build_resource_uri(
            project_name, environment_name, product_name, resource_name
        )

        # Step 1: Check if the connection info should be fetched from a mounted volume
        if config.env.connection_path is not None:
            local_resource_path = os.path.join(
                config.env.connection_path, resource_name, "latest"
            )
            if not os.path.exists(local_resource_path):
                logging.warning(
                    f"Connection info for resource '{resource_uri}' not found on disk."
                )
            else:
                with open(local_resource_path) as f:
                    return yaml.load(f, Loader=yaml.FullLoader)

        # Step 2: Check the cache for connection info, otherwise fetch from remote
        resource_connection_info = cache.get_resource_connection_info(
            project_name, environment_name, product_name, resource_name
        )
        if resource_connection_info is not None:
            logging.debug(f"Using cached resource connection info for {resource_uri}")
            return resource_connection_info

        # Step 3: Check the cache for bucket info, otherwise fetch from remote
        connection_bucket_path = cache.get_resource_connection_bucket_path(
            project_name, environment_name, product_name, resource_name
        )
        if connection_bucket_path is None:
            logging.debug(
                f"Fetching bucket connection info from remote server for {resource_uri}"
            )
            resource_info = await self.client.resources.get(
                project_name=project_name,
                environment_name=environment_name,
                resource_name=resource_name,
                product_name_to_validate=product_name,
            )
            if resource_info.connection_bucket_path is None:
                raise exceptions.RemoteConnectionInfoMissing(resource_info)
            connection_bucket_path = resource_info.connection_bucket_path
            cache.set_resource_connection_bucket_path(
                project_name,
                environment_name,
                product_name,
                resource_name,
                connection_bucket_path,
            )
        else:
            logging.debug(f"Using cached bucket connection info for {resource_uri}")

        # Step 4: Fetch the resource connection info from the remote storage bucket
        try:
            # TODO: Support async file reading (fsspec supports it)
            with fsspec.open(connection_bucket_path, mode="r") as file:
                resource_connection_info = yaml.safe_load(file.read())
        except FileNotFoundError:
            raise exceptions.ConnectionInfoNotFound(resource_name)

        # Step 5: Cache the resource connection info
        cache.set_resource_connection_info(
            project_name,
            environment_name,
            product_name,
            resource_name,
            resource_connection_info,
        )

        # Step 6: Return the resource connection info
        return resource_connection_info

    async def create_resource_operation(
        self,
        product_name: str,
        resource_name: str,
        create_args: Dict,
        project_name: Optional[str] = None,
        environment_name: Optional[str] = None,
        replace: bool = False,
    ):
        project_name = project_name or config.project
        environment_name = environment_name or config.environment
        if project_name is None or environment_name is None:
            raise exceptions.ProjectOrEnvironmentNotSet(project_name, environment_name)

        try:
            existing_resource = await self.client.resources.get(
                project_name=project_name,
                environment_name=environment_name,
                resource_name=resource_name,
                product_name_to_validate=product_name,
            )
        except exceptions.LaunchFlowRequestFailure as e:
            if e.status_code != 404:
                raise
            existing_resource = None

        if existing_resource and existing_resource.create_args == create_args:
            logging.debug(
                f"Resource '{resource_name}' already exists with the same create args"
            )
            return AsyncNoOp(
                resource_ref=f"Resource(name={resource_name})",
            )

        elif existing_resource:
            if not replace:
                raise exceptions.ResourceReplacementRequired(resource_name)

            async def replace_operation():
                # NOTE: We attempt to clear the cache info when the op is applied, but
                # swallow any exceptions since its not critical to the operation
                maybe_clear_resource_cache(
                    project_name, environment_name, product_name, resource_name
                )
                return await self.client.resources.replace(
                    project_name=project_name,
                    environment_name=environment_name,
                    product_name=product_name,
                    resource_name=resource_name,
                    create_args=create_args,
                )

            return AsyncResourceOp(
                resource_ref=f"Resource(name={resource_name})",
                operation_id=None,
                client=self.client,
                _op=replace_operation,
                _type="replace",
                create_args=create_args,
                replace_args=existing_resource.create_args,
            )

        else:

            async def create_operation():
                # NOTE: We attempt to clear the cache info when the op is applied, but
                # swallow any exceptions since its not critical to the operation
                maybe_clear_resource_cache(
                    project_name, environment_name, product_name, resource_name
                )
                return await self.client.resources.create(
                    project_name=project_name,
                    environment_name=environment_name,
                    product_name=product_name,
                    resource_name=resource_name,
                    create_args=create_args,
                )

            return AsyncResourceOp(
                resource_ref=f"Resource(name={resource_name})",
                operation_id=None,
                client=self.client,
                _op=create_operation,
                _type="create",
            )
