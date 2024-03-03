from enum import Enum
from typing import List, Optional

import beaupy
import rich
from launchflow.flows.project_flows import get_project


class Framework(Enum):
    FASTAPI = "fastapi"
    FLASK = "flask"
    DJANGO = "django"


FRAMEWORK_CHOICES = [
    (
        Framework.FASTAPI,
        "FastAPI framework, high performance, easy to learn, fast to code, ready for production",
    ),
    # (
    #     Framework.FLASK,
    #     "The Python micro framework for building web applications.",
    # ),
    # (
    #     Framework.DJANGO,
    #     "The Web framework for perfectionists with deadlines.",
    # ),
]


class Resource(Enum):
    POSTGRESQL = "PostgreSQL"
    MYSQL = "MySQL"
    PUBSUB = "PubSub"
    STORAGE_BUCKET = "StorageBucket"
    REDIS_VM = "RedisVM"
    REDIS = "Redis"

    def get_var_name(self):
        if self == Resource.POSTGRESQL:
            return "pg"
        elif self == Resource.STORAGE_BUCKET:
            return "bucket"
        elif self == Resource.REDIS_VM:
            return "redis_vm"
        elif self == Resource.REDIS:
            return "redis"
        elif self == Resource.MYSQL:
            return "mysql"
        elif self == Resource.PUBSUB:
            return "pubsub"
        else:
            raise NotImplementedError(f"{self} is not supported yet.")


RESOURCE_CHOICES = [
    (
        Resource.POSTGRESQL,
        "PostgreSQL database. Powered by Cloud SQL on GCP and RDS on AWS.",
    ),
    (
        Resource.STORAGE_BUCKET,
        "Storage bucket. Powered by Cloud Storage on GCP and S3 on AWS.",
    ),
    (
        Resource.REDIS_VM,
        "Redis on a VM. Powered by Compute Engine on GCP and EC2 on AWS.",
    ),
    (
        Resource.REDIS,
        "Redis Cluster. Powered by Cloud Memorystore on GCP and ElastiCache on AWS.",
    ),
    # (Resource.MYSQL, "MySQL database. Powered by Cloud SQL on GCP and RDS on AWS."),
    # (Resource.PUBSUB, "PubSub messaging. Powered by Cloud PubSub on GCP and AWS SQS."),
]


def project(account_id: Optional[str]):
    print()
    print("Welcome to launchflow!")
    print("This tool will help you create a new application.")
    print("Let's get started!")
    print()
    return get_project(project_name=None, prompt_for_creation=True)


def framework() -> Framework:
    options = [f"{f[0].value} - {f[1]}" for f in FRAMEWORK_CHOICES]
    print()
    print("Select a framework for your API: (More coming soon)")
    answer = beaupy.select(options=options, return_index=True)
    rich.print(f"[pink1]>[/pink1] {options[answer]}")
    return FRAMEWORK_CHOICES[answer][0]


def resources() -> List[Resource]:
    options = [f"{f[0].value} - {f[1]}" for f in RESOURCE_CHOICES]
    print()
    print(
        "Select any resources you want to include in your application. These resources will be created in your cloud provider account:"
    )
    answers = beaupy.select_multiple(options=options, return_indices=True)
    to_ret = []
    for answer in answers:
        rich.print(f"[pink1]>[/pink1] {options[answer]}")
        to_ret.append(RESOURCE_CHOICES[answer][0])
    if not answers:
        rich.print("[pink1]>[/pink1] No resources selected.")
    return to_ret


def environments() -> List[str]:
    print()
    environments = []
    print(
        "Enter environments (dev, staging, prod) to include (leave blank to continue):"
    )
    while True:
        env = beaupy.prompt("")
        if not env:
            if not environments:
                print("At least one environment is required.")
                continue
            break
        environments.append(env)
        rich.print(f"[pink1]>[/pink1] {env}")
    return environments


def requirements(framework: Framework, resources: List[Resource]):
    # TODO: Remove the gcp hardcoding once we have AWS / Azure support
    requirements = set(["launchflow[gcp]"])
    if framework == Framework.FASTAPI:
        requirements.update(["fastapi", "uvicorn"])
    elif framework == Framework.FLASK:
        requirements.add("flask")
    elif framework == Framework.DJANGO:
        requirements.add("django")
    else:
        raise NotImplementedError(f"{framework} is not supported yet.")
    if Resource.POSTGRESQL in resources:
        requirements.add("pg8000")
        requirements.add("sqlalchemy")
    if Resource.MYSQL in resources:
        requirements.add("pymysql")
        requirements.add("sqlalchemy")
    if Resource.REDIS_VM in resources or Resource.REDIS in resources:
        requirements.add("redis")
    requirements = list(requirements)
    requirements.sort()
    return "\n".join(requirements)
