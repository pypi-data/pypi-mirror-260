# ruff: noqa
import contextlib

from .client import LaunchFlowAsyncClient, LaunchFlowClient

launchflow_client = None


# TODO: Update calling code to close the client when done or use the context manager
def get_launchflow_client_legacy() -> LaunchFlowClient:
    global launchflow_client
    if not launchflow_client:
        launchflow_client = LaunchFlowClient()
    return launchflow_client


@contextlib.contextmanager
def launchflow_client_ctx():
    launchflow_client = LaunchFlowClient()
    try:
        yield launchflow_client
    finally:
        launchflow_client.close()


@contextlib.asynccontextmanager
async def async_launchflow_client_ctx():
    launchflow_async_client = LaunchFlowAsyncClient()
    try:
        yield launchflow_async_client
    finally:
        await launchflow_async_client.close()
