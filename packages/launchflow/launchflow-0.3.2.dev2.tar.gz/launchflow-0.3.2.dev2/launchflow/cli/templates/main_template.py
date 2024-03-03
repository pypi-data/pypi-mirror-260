from typing import List

from launchflow.cli.project_gen import Framework, Resource

FAST_API_TEMPLATE = """\
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {{"message": "Hello World"}}
"""

# TODO: look at adding templates for using the provided resources
FAST_API_TEMPLATE_WITH_RESOURCES = """\
from contextlib import asynccontextmanager

from fastapi import FastAPI{lf_resource_imports}


@asynccontextmanager
async def lifespan(app: FastAPI):
    {lf_resource_connections}
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def root():
    return {{"message": "Hello World"}}
"""


def template(framework: Framework, resources: List[Resource]):

    if framework == Framework.FASTAPI:

        if not resources:
            return FAST_API_TEMPLATE

        lf_resource_imports = "\nfrom infra import " + ", ".join(
            [r.get_var_name() for r in resources]
        )
        lf_resource_connections = "\n".join(
            [f"await {r.get_var_name()}.connect_async()" for r in resources]
        )
        return FAST_API_TEMPLATE_WITH_RESOURCES.format(
            lf_resource_imports=lf_resource_imports,
            lf_resource_connections=lf_resource_connections,
        )

    else:
        raise ValueError(f"Framework: {framework} is not supported yet.")
