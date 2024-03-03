from typing import Generic, Optional, TypeVar, get_args

from launchflow.context import async_ctx, ctx
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


# TODO: Add autodocs / examples for this class
class Resource(Generic[T]):
    def __init__(self, name: str, product_name: str, create_args: dict):
        self.name = name
        self._product_name = product_name
        self._create_args = create_args

        self._connection_info: Optional[T] = None
        # This line extracts the type argument from the Generic base
        self._connection_type: T = get_args(self.__class__.__orig_bases__[0])[0]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, connected={self._connection_info is not None})"  # noqa

    def connect(self):
        """
        Synchronously connect to the resource by fetching its connection info.
        """
        connection_info = ctx.get_resource_connection_info(
            product_name=self._product_name,
            resource_name=self.name,
        )
        return self._connection_type.model_validate(connection_info)

    async def connect_async(self):
        """
        Asynchronously connect to the resource by fetching its connection info.
        """
        connection_info = await async_ctx.get_resource_connection_info(
            product_name=self._product_name,
            resource_name=self.name,
        )
        return self._connection_type.model_validate(connection_info)

    def create(
        self,
        *,
        project_name: str = None,
        environment_name: str = None,
        replace: bool = False,
    ):
        """
        Synchronously create the resource.
        """
        return ctx.create_resource_operation(
            product_name=self._product_name,
            resource_name=self.name,
            create_args=self._create_args,
            project_name=project_name,
            environment_name=environment_name,
            replace=replace,
        )

    async def create_async(
        self,
        *,
        project_name: str = None,
        environment_name: str = None,
        replace: bool = False,
    ):
        """
        Asynchronously create the resource.
        """
        return await async_ctx.create_resource_operation(
            product_name=self._product_name,
            resource_name=self.name,
            create_args=self._create_args,
            project_name=project_name,
            environment_name=environment_name,
            replace=replace,
        )
