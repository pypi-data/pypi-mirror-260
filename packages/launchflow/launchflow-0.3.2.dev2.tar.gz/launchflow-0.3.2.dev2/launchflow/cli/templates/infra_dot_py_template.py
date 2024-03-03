from typing import List

from launchflow.cli.project_gen import Framework, Resource

LAUNCH_TEMPLATE = """\
import launchflow as lf

{resources}
"""


# TODO: Support dynamic cloud provider (currently hard coded to GCP)
def template(project: str, framework: str, resources: List[Resource]):
    if framework == Framework.FASTAPI:
        entrypoint = '"uvicorn main:app"'
    else:
        raise NotImplementedError(f"{framework} is not supported yet.")

    resource_strs = []
    resource_vars = []
    for resource in resources:
        resource_vars.append(resource.get_var_name())

        if resource == Resource.POSTGRESQL:
            resource_strs.append(
                "# Docs: https://docs.launchflow.com/reference/gcp-resources/cloud-sql"
            )
            resource_strs.append(
                f'pg = lf.gcp.CloudSQLPostgres("{project}-postgres")\n'
            )
        elif resource == Resource.STORAGE_BUCKET:
            resource_strs.append(
                "# Docs: https://docs.launchflow.com/reference/gcp-resources/gcs-bucket"
            )
            resource_strs.append(f'bucket = lf.gcp.GCSBucket("{project}-bucket")\n')
        elif resource == Resource.REDIS_VM:
            resource_strs.append(
                "# Docs: https://docs.launchflow.com/reference/gcp-resources/compute-engine"
            )
            resource_strs.append(
                f'redis_vm = lf.gcp.ComputeEngineRedis("{project}-redis-vm")\n'
            )
        elif resource == Resource.REDIS:
            resource_strs.append(
                "# Docs: https://docs.launchflow.com/reference/gcp-resources/memorystore"
            )
            resource_strs.append(
                f'redis = lf.gcp.MemorystoreRedis("{project}-redis")\n'
            )
        else:
            raise NotImplementedError(f"{resource} is not supported yet.")

    env = []
    if not resource_vars:
        env = "dev = launchflow.Environment([app])"
    else:
        env = f"dev = launchflow.Environment([app], [{', '.join(resource_vars)}])"
    return LAUNCH_TEMPLATE.format(
        project=project,
        entrypoint=entrypoint,
        resources=("\n" + "\n".join(resource_strs)) if resource_strs else "",
        environment=env,
    )
