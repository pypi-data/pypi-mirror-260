import datetime
import enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


# TODO: figure out how to better parse enums so we can make these lowercase
class OperationStatus(enum.Enum):
    UNKNOWN = "UNKNOWN"
    PENDING = "PENDING"
    QUEUED = "QUEUED"
    WORKING = "WORKING"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    TIMEOUT = "TIMEOUT"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"

    def is_final(self):
        return self in [
            OperationStatus.SUCCESS,
            OperationStatus.FAILURE,
            OperationStatus.CANCELLED,
            OperationStatus.EXPIRED,
            OperationStatus.TIMEOUT,
            OperationStatus.INTERNAL_ERROR,
        ]

    def is_error(self):
        return self in [
            OperationStatus.FAILURE,
            OperationStatus.INTERNAL_ERROR,
            OperationStatus.TIMEOUT,
        ]

    def is_success(self):
        return self == OperationStatus.SUCCESS

    def is_cancelled(self):
        return self == OperationStatus.CANCELLED


class OperationResponse(BaseModel):
    id: str
    status: OperationStatus


class ResourceResponse(BaseModel):
    name: str
    cloud_provider: str
    resource_product: str
    status: str
    status_message: Optional[str]
    create_args: Dict[str, Any]
    connection_bucket_path: Optional[str]

    def __str__(self) -> str:
        return f"Resource(name='{self.name}', resource_product='{self.resource_product}', status='{self.status}')"


class ProjectResponse(BaseModel):
    name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    configured_cloud_providers: List[str]


class GCPEnvironmentConfigResponse(BaseModel):
    created_at: datetime.datetime
    updated_at: datetime.datetime
    gcp_project_id: str
    gcp_service_account_email: str
    default_gcp_region: str
    default_gcp_zone: str
    artifact_bucket: str


class AWSEnvironmentConfigResponse(BaseModel):
    created_at: datetime.datetime
    updated_at: datetime.datetime
    aws_region: str
    aws_zones: List[str]
    aws_iam_role_arn: str
    aws_vpc_id: str
    artifact_bucket: str


class EnvironmentType(enum.Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"


class EnvironmentResponse(BaseModel):
    name: str
    environment_type: EnvironmentType
    created_at: datetime.datetime
    updated_at: datetime.datetime
    gcp_config: Optional[GCPEnvironmentConfigResponse] = None
    aws_config: Optional[AWSEnvironmentConfigResponse] = None

    resources: Dict[str, ResourceResponse] = {}


class AccountResponse(BaseModel):
    id: str


class GCPConnectionInfoResponse(BaseModel):
    verified_at: Optional[datetime.datetime]
    admin_service_account_email: str


class AWSConnectionInfoResponse(BaseModel):
    verified_at: Optional[datetime.datetime]
    external_role_id: str
    cloud_foundation_template_url: Optional[str]


class ConnectionInfoResponse(BaseModel):
    gcp_connection_info: GCPConnectionInfoResponse
    aws_connection_info: AWSConnectionInfoResponse
