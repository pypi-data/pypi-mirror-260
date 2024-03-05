from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DeploymentStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AWAITING_WORKFLOW_START: _ClassVar[DeploymentStatus]
    PROVISIONING_RESOURCES_FOR_CREATE: _ClassVar[DeploymentStatus]
    PROVISIONING_RESOURCES_FOR_UPDATE: _ClassVar[DeploymentStatus]
    COMPLETED: _ClassVar[DeploymentStatus]
    DELETING_RESOURCES: _ClassVar[DeploymentStatus]
    DELETED: _ClassVar[DeploymentStatus]
    FAILURE: _ClassVar[DeploymentStatus]
    ALL_STATUS_TYPES: _ClassVar[DeploymentStatus]

class PasswordInstantiationBehavior(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DEFAULT: _ClassVar[PasswordInstantiationBehavior]
    SEND_RESET_EMAIL: _ClassVar[PasswordInstantiationBehavior]
    GENERATE_RESET_LINK: _ClassVar[PasswordInstantiationBehavior]

class TenantPlannedUse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TP_DEFAULT: _ClassVar[TenantPlannedUse]
    TP_PERSONAL: _ClassVar[TenantPlannedUse]
    TP_WORK: _ClassVar[TenantPlannedUse]
AWAITING_WORKFLOW_START: DeploymentStatus
PROVISIONING_RESOURCES_FOR_CREATE: DeploymentStatus
PROVISIONING_RESOURCES_FOR_UPDATE: DeploymentStatus
COMPLETED: DeploymentStatus
DELETING_RESOURCES: DeploymentStatus
DELETED: DeploymentStatus
FAILURE: DeploymentStatus
ALL_STATUS_TYPES: DeploymentStatus
DEFAULT: PasswordInstantiationBehavior
SEND_RESET_EMAIL: PasswordInstantiationBehavior
GENERATE_RESET_LINK: PasswordInstantiationBehavior
TP_DEFAULT: TenantPlannedUse
TP_PERSONAL: TenantPlannedUse
TP_WORK: TenantPlannedUse

class ManagementPingRequest(_message.Message):
    __slots__ = ("test_string",)
    TEST_STRING_FIELD_NUMBER: _ClassVar[int]
    test_string: str
    def __init__(self, test_string: _Optional[str] = ...) -> None: ...

class ManagementPingResponse(_message.Message):
    __slots__ = ("test_string_back",)
    TEST_STRING_BACK_FIELD_NUMBER: _ClassVar[int]
    test_string_back: str
    def __init__(self, test_string_back: _Optional[str] = ...) -> None: ...

class CreateTenantRequest(_message.Message):
    __slots__ = ("customer_profile", "account", "request_audit_user_info")
    CUSTOMER_PROFILE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    REQUEST_AUDIT_USER_INFO_FIELD_NUMBER: _ClassVar[int]
    customer_profile: str
    account: str
    request_audit_user_info: RequestAuditUserInfo
    def __init__(self, customer_profile: _Optional[str] = ..., account: _Optional[str] = ..., request_audit_user_info: _Optional[_Union[RequestAuditUserInfo, _Mapping]] = ...) -> None: ...

class CreateTenantResponse(_message.Message):
    __slots__ = ("tenant_id",)
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    tenant_id: str
    def __init__(self, tenant_id: _Optional[str] = ...) -> None: ...

class GetTenantRequest(_message.Message):
    __slots__ = ("tenant_id", "deployment_status")
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_STATUS_FIELD_NUMBER: _ClassVar[int]
    tenant_id: str
    deployment_status: DeploymentStatus
    def __init__(self, tenant_id: _Optional[str] = ..., deployment_status: _Optional[_Union[DeploymentStatus, str]] = ...) -> None: ...

class GetTenantResponse(_message.Message):
    __slots__ = ("tenant_metadata", "tenant_deployments")
    TENANT_METADATA_FIELD_NUMBER: _ClassVar[int]
    TENANT_DEPLOYMENTS_FIELD_NUMBER: _ClassVar[int]
    tenant_metadata: TenantMetadata
    tenant_deployments: _containers.RepeatedCompositeFieldContainer[TenantDeployment]
    def __init__(self, tenant_metadata: _Optional[_Union[TenantMetadata, _Mapping]] = ..., tenant_deployments: _Optional[_Iterable[_Union[TenantDeployment, _Mapping]]] = ...) -> None: ...

class TenantMetadata(_message.Message):
    __slots__ = ("id", "customer_profile", "account", "tms_create_utc", "tms_update_utc", "name", "company_info")
    ID_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_PROFILE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    TMS_CREATE_UTC_FIELD_NUMBER: _ClassVar[int]
    TMS_UPDATE_UTC_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    COMPANY_INFO_FIELD_NUMBER: _ClassVar[int]
    id: str
    customer_profile: str
    account: str
    tms_create_utc: _timestamp_pb2.Timestamp
    tms_update_utc: _timestamp_pb2.Timestamp
    name: str
    company_info: CompanyInfo
    def __init__(self, id: _Optional[str] = ..., customer_profile: _Optional[str] = ..., account: _Optional[str] = ..., tms_create_utc: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., tms_update_utc: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., name: _Optional[str] = ..., company_info: _Optional[_Union[CompanyInfo, _Mapping]] = ...) -> None: ...

class TenantDeployment(_message.Message):
    __slots__ = ("id", "aws_ami_deployment_info", "tms_create_utc", "tms_update_utc", "app_version", "terraform_script_id", "deployment_workflow_run_id", "deployment_status", "environment", "vpc")
    ID_FIELD_NUMBER: _ClassVar[int]
    AWS_AMI_DEPLOYMENT_INFO_FIELD_NUMBER: _ClassVar[int]
    TMS_CREATE_UTC_FIELD_NUMBER: _ClassVar[int]
    TMS_UPDATE_UTC_FIELD_NUMBER: _ClassVar[int]
    APP_VERSION_FIELD_NUMBER: _ClassVar[int]
    TERRAFORM_SCRIPT_ID_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_WORKFLOW_RUN_ID_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_STATUS_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    VPC_FIELD_NUMBER: _ClassVar[int]
    id: str
    aws_ami_deployment_info: AwsAmiDeploymentInfo
    tms_create_utc: _timestamp_pb2.Timestamp
    tms_update_utc: _timestamp_pb2.Timestamp
    app_version: str
    terraform_script_id: str
    deployment_workflow_run_id: str
    deployment_status: str
    environment: str
    vpc: str
    def __init__(self, id: _Optional[str] = ..., aws_ami_deployment_info: _Optional[_Union[AwsAmiDeploymentInfo, _Mapping]] = ..., tms_create_utc: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., tms_update_utc: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., app_version: _Optional[str] = ..., terraform_script_id: _Optional[str] = ..., deployment_workflow_run_id: _Optional[str] = ..., deployment_status: _Optional[str] = ..., environment: _Optional[str] = ..., vpc: _Optional[str] = ...) -> None: ...

class AwsAmiDeploymentInfo(_message.Message):
    __slots__ = ("id", "region", "account_id", "terraform_state_path", "vmcount", "vmsize", "volsize", "tms_create_utc", "tms_update_utc", "instance_id", "route_53_entry", "ebs_volume_id", "volume_attachment_id", "launch_template_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    TERRAFORM_STATE_PATH_FIELD_NUMBER: _ClassVar[int]
    VMCOUNT_FIELD_NUMBER: _ClassVar[int]
    VMSIZE_FIELD_NUMBER: _ClassVar[int]
    VOLSIZE_FIELD_NUMBER: _ClassVar[int]
    TMS_CREATE_UTC_FIELD_NUMBER: _ClassVar[int]
    TMS_UPDATE_UTC_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    ROUTE_53_ENTRY_FIELD_NUMBER: _ClassVar[int]
    EBS_VOLUME_ID_FIELD_NUMBER: _ClassVar[int]
    VOLUME_ATTACHMENT_ID_FIELD_NUMBER: _ClassVar[int]
    LAUNCH_TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    region: str
    account_id: str
    terraform_state_path: str
    vmcount: int
    vmsize: str
    volsize: str
    tms_create_utc: _timestamp_pb2.Timestamp
    tms_update_utc: _timestamp_pb2.Timestamp
    instance_id: str
    route_53_entry: str
    ebs_volume_id: str
    volume_attachment_id: str
    launch_template_id: str
    def __init__(self, id: _Optional[str] = ..., region: _Optional[str] = ..., account_id: _Optional[str] = ..., terraform_state_path: _Optional[str] = ..., vmcount: _Optional[int] = ..., vmsize: _Optional[str] = ..., volsize: _Optional[str] = ..., tms_create_utc: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., tms_update_utc: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., instance_id: _Optional[str] = ..., route_53_entry: _Optional[str] = ..., ebs_volume_id: _Optional[str] = ..., volume_attachment_id: _Optional[str] = ..., launch_template_id: _Optional[str] = ...) -> None: ...

class ListTenantsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListTenantsResponse(_message.Message):
    __slots__ = ("matching_tenants",)
    MATCHING_TENANTS_FIELD_NUMBER: _ClassVar[int]
    matching_tenants: _containers.RepeatedCompositeFieldContainer[TenantMetadata]
    def __init__(self, matching_tenants: _Optional[_Iterable[_Union[TenantMetadata, _Mapping]]] = ...) -> None: ...

class SearchTenantRequest(_message.Message):
    __slots__ = ("customer_profile", "account")
    CUSTOMER_PROFILE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    customer_profile: str
    account: str
    def __init__(self, customer_profile: _Optional[str] = ..., account: _Optional[str] = ...) -> None: ...

class CreateTenantDeploymentRequest(_message.Message):
    __slots__ = ("tenant_id", "description", "environment", "vpc", "region", "app_version", "rdata_version", "rdata_type", "vmsize", "volsize", "config_override_mode", "use_staging_certificate", "use_zerossl_cert", "enable_auth0_signup", "include_truera_aad_connection", "logging_and_tracing_options", "request_audit_user_info")
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    VPC_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    APP_VERSION_FIELD_NUMBER: _ClassVar[int]
    RDATA_VERSION_FIELD_NUMBER: _ClassVar[int]
    RDATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    VMSIZE_FIELD_NUMBER: _ClassVar[int]
    VOLSIZE_FIELD_NUMBER: _ClassVar[int]
    CONFIG_OVERRIDE_MODE_FIELD_NUMBER: _ClassVar[int]
    USE_STAGING_CERTIFICATE_FIELD_NUMBER: _ClassVar[int]
    USE_ZEROSSL_CERT_FIELD_NUMBER: _ClassVar[int]
    ENABLE_AUTH0_SIGNUP_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_TRUERA_AAD_CONNECTION_FIELD_NUMBER: _ClassVar[int]
    LOGGING_AND_TRACING_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    REQUEST_AUDIT_USER_INFO_FIELD_NUMBER: _ClassVar[int]
    tenant_id: str
    description: str
    environment: str
    vpc: str
    region: str
    app_version: str
    rdata_version: str
    rdata_type: str
    vmsize: str
    volsize: str
    config_override_mode: str
    use_staging_certificate: bool
    use_zerossl_cert: bool
    enable_auth0_signup: bool
    include_truera_aad_connection: bool
    logging_and_tracing_options: str
    request_audit_user_info: RequestAuditUserInfo
    def __init__(self, tenant_id: _Optional[str] = ..., description: _Optional[str] = ..., environment: _Optional[str] = ..., vpc: _Optional[str] = ..., region: _Optional[str] = ..., app_version: _Optional[str] = ..., rdata_version: _Optional[str] = ..., rdata_type: _Optional[str] = ..., vmsize: _Optional[str] = ..., volsize: _Optional[str] = ..., config_override_mode: _Optional[str] = ..., use_staging_certificate: bool = ..., use_zerossl_cert: bool = ..., enable_auth0_signup: bool = ..., include_truera_aad_connection: bool = ..., logging_and_tracing_options: _Optional[str] = ..., request_audit_user_info: _Optional[_Union[RequestAuditUserInfo, _Mapping]] = ...) -> None: ...

class CreateTenantDeploymentResponse(_message.Message):
    __slots__ = ("tenant_deployment_id", "workflow_id")
    TENANT_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    WORKFLOW_ID_FIELD_NUMBER: _ClassVar[int]
    tenant_deployment_id: str
    workflow_id: str
    def __init__(self, tenant_deployment_id: _Optional[str] = ..., workflow_id: _Optional[str] = ...) -> None: ...

class GetTenantDeploymentRequest(_message.Message):
    __slots__ = ("tenant_deployment_id",)
    TENANT_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    tenant_deployment_id: str
    def __init__(self, tenant_deployment_id: _Optional[str] = ...) -> None: ...

class GetTenantDeploymentResponse(_message.Message):
    __slots__ = ("tenant_deployment",)
    TENANT_DEPLOYMENT_FIELD_NUMBER: _ClassVar[int]
    tenant_deployment: TenantDeployment
    def __init__(self, tenant_deployment: _Optional[_Union[TenantDeployment, _Mapping]] = ...) -> None: ...

class UpdateTenantDeploymentRequest(_message.Message):
    __slots__ = ("tenant_deployment_id", "app_version", "vmsize", "config_override_mode", "use_staging_certificate", "use_zerossl_cert", "logging_and_tracing_options", "request_audit_user_info")
    TENANT_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    APP_VERSION_FIELD_NUMBER: _ClassVar[int]
    VMSIZE_FIELD_NUMBER: _ClassVar[int]
    CONFIG_OVERRIDE_MODE_FIELD_NUMBER: _ClassVar[int]
    USE_STAGING_CERTIFICATE_FIELD_NUMBER: _ClassVar[int]
    USE_ZEROSSL_CERT_FIELD_NUMBER: _ClassVar[int]
    LOGGING_AND_TRACING_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    REQUEST_AUDIT_USER_INFO_FIELD_NUMBER: _ClassVar[int]
    tenant_deployment_id: str
    app_version: str
    vmsize: str
    config_override_mode: str
    use_staging_certificate: bool
    use_zerossl_cert: bool
    logging_and_tracing_options: str
    request_audit_user_info: RequestAuditUserInfo
    def __init__(self, tenant_deployment_id: _Optional[str] = ..., app_version: _Optional[str] = ..., vmsize: _Optional[str] = ..., config_override_mode: _Optional[str] = ..., use_staging_certificate: bool = ..., use_zerossl_cert: bool = ..., logging_and_tracing_options: _Optional[str] = ..., request_audit_user_info: _Optional[_Union[RequestAuditUserInfo, _Mapping]] = ...) -> None: ...

class UpdateTenantDeploymentResponse(_message.Message):
    __slots__ = ("tenant_deployment_id", "workflow_id")
    TENANT_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    WORKFLOW_ID_FIELD_NUMBER: _ClassVar[int]
    tenant_deployment_id: str
    workflow_id: str
    def __init__(self, tenant_deployment_id: _Optional[str] = ..., workflow_id: _Optional[str] = ...) -> None: ...

class DeleteTenantDeploymentRequest(_message.Message):
    __slots__ = ("tenant_deployment_id", "request_audit_user_info")
    TENANT_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_AUDIT_USER_INFO_FIELD_NUMBER: _ClassVar[int]
    tenant_deployment_id: str
    request_audit_user_info: RequestAuditUserInfo
    def __init__(self, tenant_deployment_id: _Optional[str] = ..., request_audit_user_info: _Optional[_Union[RequestAuditUserInfo, _Mapping]] = ...) -> None: ...

class DeleteTenantDeploymentResponse(_message.Message):
    __slots__ = ("tenant_deployment_id", "workflow_id")
    TENANT_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    WORKFLOW_ID_FIELD_NUMBER: _ClassVar[int]
    tenant_deployment_id: str
    workflow_id: str
    def __init__(self, tenant_deployment_id: _Optional[str] = ..., workflow_id: _Optional[str] = ...) -> None: ...

class AddUserToTenantRequest(_message.Message):
    __slots__ = ("email", "name", "password", "tenant_id", "password_instantiation_behavior", "request_audit_user_info")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_INSTANTIATION_BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    REQUEST_AUDIT_USER_INFO_FIELD_NUMBER: _ClassVar[int]
    email: str
    name: str
    password: str
    tenant_id: str
    password_instantiation_behavior: PasswordInstantiationBehavior
    request_audit_user_info: RequestAuditUserInfo
    def __init__(self, email: _Optional[str] = ..., name: _Optional[str] = ..., password: _Optional[str] = ..., tenant_id: _Optional[str] = ..., password_instantiation_behavior: _Optional[_Union[PasswordInstantiationBehavior, str]] = ..., request_audit_user_info: _Optional[_Union[RequestAuditUserInfo, _Mapping]] = ...) -> None: ...

class AddUserToTenantResponse(_message.Message):
    __slots__ = ("email", "password", "tenant_id", "workflow_id")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    WORKFLOW_ID_FIELD_NUMBER: _ClassVar[int]
    email: str
    password: str
    tenant_id: str
    workflow_id: str
    def __init__(self, email: _Optional[str] = ..., password: _Optional[str] = ..., tenant_id: _Optional[str] = ..., workflow_id: _Optional[str] = ...) -> None: ...

class ListAuth0UsersOfTenantRequest(_message.Message):
    __slots__ = ("tenant_id",)
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    tenant_id: str
    def __init__(self, tenant_id: _Optional[str] = ...) -> None: ...

class ListAuth0UsersOfTenantResponse(_message.Message):
    __slots__ = ("auth0_users",)
    AUTH0_USERS_FIELD_NUMBER: _ClassVar[int]
    auth0_users: _containers.RepeatedCompositeFieldContainer[Auth0User]
    def __init__(self, auth0_users: _Optional[_Iterable[_Union[Auth0User, _Mapping]]] = ...) -> None: ...

class Auth0User(_message.Message):
    __slots__ = ("name", "email", "email_verified")
    NAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    EMAIL_VERIFIED_FIELD_NUMBER: _ClassVar[int]
    name: str
    email: str
    email_verified: bool
    def __init__(self, name: _Optional[str] = ..., email: _Optional[str] = ..., email_verified: bool = ...) -> None: ...

class TriggerPasswordResetForUserRequest(_message.Message):
    __slots__ = ("email", "tenant_id", "password_instantiation_behavior", "request_audit_user_info")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_INSTANTIATION_BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    REQUEST_AUDIT_USER_INFO_FIELD_NUMBER: _ClassVar[int]
    email: str
    tenant_id: str
    password_instantiation_behavior: PasswordInstantiationBehavior
    request_audit_user_info: RequestAuditUserInfo
    def __init__(self, email: _Optional[str] = ..., tenant_id: _Optional[str] = ..., password_instantiation_behavior: _Optional[_Union[PasswordInstantiationBehavior, str]] = ..., request_audit_user_info: _Optional[_Union[RequestAuditUserInfo, _Mapping]] = ...) -> None: ...

class TriggerPasswordResetForUserResponse(_message.Message):
    __slots__ = ("email", "tenant_id", "workflow_id")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    WORKFLOW_ID_FIELD_NUMBER: _ClassVar[int]
    email: str
    tenant_id: str
    workflow_id: str
    def __init__(self, email: _Optional[str] = ..., tenant_id: _Optional[str] = ..., workflow_id: _Optional[str] = ...) -> None: ...

class DeleteUserFromTenantRequest(_message.Message):
    __slots__ = ("email", "tenant_id", "request_audit_user_info")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_AUDIT_USER_INFO_FIELD_NUMBER: _ClassVar[int]
    email: str
    tenant_id: str
    request_audit_user_info: RequestAuditUserInfo
    def __init__(self, email: _Optional[str] = ..., tenant_id: _Optional[str] = ..., request_audit_user_info: _Optional[_Union[RequestAuditUserInfo, _Mapping]] = ...) -> None: ...

class DeleteUserFromTenantResponse(_message.Message):
    __slots__ = ("email", "tenant_id", "workflow_id")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    WORKFLOW_ID_FIELD_NUMBER: _ClassVar[int]
    email: str
    tenant_id: str
    workflow_id: str
    def __init__(self, email: _Optional[str] = ..., tenant_id: _Optional[str] = ..., workflow_id: _Optional[str] = ...) -> None: ...

class RequestAuditUserInfo(_message.Message):
    __slots__ = ("email", "name")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    email: str
    name: str
    def __init__(self, email: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class GetTenantConfigRequest(_message.Message):
    __slots__ = ("tenant_id",)
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    tenant_id: str
    def __init__(self, tenant_id: _Optional[str] = ...) -> None: ...

class GetTenantConfigResponse(_message.Message):
    __slots__ = ("tenant_config",)
    TENANT_CONFIG_FIELD_NUMBER: _ClassVar[int]
    tenant_config: TenantConfig
    def __init__(self, tenant_config: _Optional[_Union[TenantConfig, _Mapping]] = ...) -> None: ...

class GetAllTenantConfigsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetAllTenantConfigsResponse(_message.Message):
    __slots__ = ("tenant_configs",)
    TENANT_CONFIGS_FIELD_NUMBER: _ClassVar[int]
    tenant_configs: _containers.RepeatedCompositeFieldContainer[TenantConfig]
    def __init__(self, tenant_configs: _Optional[_Iterable[_Union[TenantConfig, _Mapping]]] = ...) -> None: ...

class UpdateTenantConfigRequest(_message.Message):
    __slots__ = ("tenant_id", "email", "service_configs", "feature_flags")
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    SERVICE_CONFIGS_FIELD_NUMBER: _ClassVar[int]
    FEATURE_FLAGS_FIELD_NUMBER: _ClassVar[int]
    tenant_id: str
    email: str
    service_configs: str
    feature_flags: str
    def __init__(self, tenant_id: _Optional[str] = ..., email: _Optional[str] = ..., service_configs: _Optional[str] = ..., feature_flags: _Optional[str] = ...) -> None: ...

class UpdateTenantConfigResponse(_message.Message):
    __slots__ = ("tenant_config",)
    TENANT_CONFIG_FIELD_NUMBER: _ClassVar[int]
    tenant_config: TenantConfig
    def __init__(self, tenant_config: _Optional[_Union[TenantConfig, _Mapping]] = ...) -> None: ...

class TenantConfig(_message.Message):
    __slots__ = ("tenant_id", "service_configs", "feature_flags", "version_id", "truera_user_id")
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    SERVICE_CONFIGS_FIELD_NUMBER: _ClassVar[int]
    FEATURE_FLAGS_FIELD_NUMBER: _ClassVar[int]
    VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    TRUERA_USER_ID_FIELD_NUMBER: _ClassVar[int]
    tenant_id: str
    service_configs: str
    feature_flags: str
    version_id: int
    truera_user_id: str
    def __init__(self, tenant_id: _Optional[str] = ..., service_configs: _Optional[str] = ..., feature_flags: _Optional[str] = ..., version_id: _Optional[int] = ..., truera_user_id: _Optional[str] = ...) -> None: ...

class SignupFormOptions(_message.Message):
    __slots__ = ("model_type_form_options", "data_type_form_options", "interest_form_options")
    MODEL_TYPE_FORM_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_FORM_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    INTEREST_FORM_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    model_type_form_options: _containers.RepeatedScalarFieldContainer[str]
    data_type_form_options: _containers.RepeatedScalarFieldContainer[str]
    interest_form_options: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, model_type_form_options: _Optional[_Iterable[str]] = ..., data_type_form_options: _Optional[_Iterable[str]] = ..., interest_form_options: _Optional[_Iterable[str]] = ...) -> None: ...

class SignUpNewTenantRequest(_message.Message):
    __slots__ = ("new_user_info", "company_info", "tier", "signup_form_options", "tenant_name", "tenant_id", "aws_marketplace_signup_info")
    NEW_USER_INFO_FIELD_NUMBER: _ClassVar[int]
    COMPANY_INFO_FIELD_NUMBER: _ClassVar[int]
    TIER_FIELD_NUMBER: _ClassVar[int]
    SIGNUP_FORM_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    TENANT_NAME_FIELD_NUMBER: _ClassVar[int]
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    AWS_MARKETPLACE_SIGNUP_INFO_FIELD_NUMBER: _ClassVar[int]
    new_user_info: NewUserInfo
    company_info: CompanyInfo
    tier: TenantInfo.SubscriptionTier
    signup_form_options: SignupFormOptions
    tenant_name: str
    tenant_id: str
    aws_marketplace_signup_info: AwsMarketplaceSignupInfo
    def __init__(self, new_user_info: _Optional[_Union[NewUserInfo, _Mapping]] = ..., company_info: _Optional[_Union[CompanyInfo, _Mapping]] = ..., tier: _Optional[_Union[TenantInfo.SubscriptionTier, str]] = ..., signup_form_options: _Optional[_Union[SignupFormOptions, _Mapping]] = ..., tenant_name: _Optional[str] = ..., tenant_id: _Optional[str] = ..., aws_marketplace_signup_info: _Optional[_Union[AwsMarketplaceSignupInfo, _Mapping]] = ...) -> None: ...

class InviteNewUserRequest(_message.Message):
    __slots__ = ("new_user_info", "tenant_id")
    NEW_USER_INFO_FIELD_NUMBER: _ClassVar[int]
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    new_user_info: NewUserInfo
    tenant_id: str
    def __init__(self, new_user_info: _Optional[_Union[NewUserInfo, _Mapping]] = ..., tenant_id: _Optional[str] = ...) -> None: ...

class AwsMarketplaceSignupInfo(_message.Message):
    __slots__ = ("is_from_aws_marketplace", "x_amzn_marketplace_token", "x_amzn_marketplace_offer_type")
    IS_FROM_AWS_MARKETPLACE_FIELD_NUMBER: _ClassVar[int]
    X_AMZN_MARKETPLACE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    X_AMZN_MARKETPLACE_OFFER_TYPE_FIELD_NUMBER: _ClassVar[int]
    is_from_aws_marketplace: bool
    x_amzn_marketplace_token: str
    x_amzn_marketplace_offer_type: str
    def __init__(self, is_from_aws_marketplace: bool = ..., x_amzn_marketplace_token: _Optional[str] = ..., x_amzn_marketplace_offer_type: _Optional[str] = ...) -> None: ...

class TenantInfo(_message.Message):
    __slots__ = ("tenant_id", "company_info", "subscription_tier")
    class SubscriptionTier(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ST_INVALID: _ClassVar[TenantInfo.SubscriptionTier]
        ST_FREE: _ClassVar[TenantInfo.SubscriptionTier]
    ST_INVALID: TenantInfo.SubscriptionTier
    ST_FREE: TenantInfo.SubscriptionTier
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    COMPANY_INFO_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTION_TIER_FIELD_NUMBER: _ClassVar[int]
    tenant_id: str
    company_info: CompanyInfo
    subscription_tier: TenantInfo.SubscriptionTier
    def __init__(self, tenant_id: _Optional[str] = ..., company_info: _Optional[_Union[CompanyInfo, _Mapping]] = ..., subscription_tier: _Optional[_Union[TenantInfo.SubscriptionTier, str]] = ...) -> None: ...

class CompanyInfo(_message.Message):
    __slots__ = ("customer_name", "organization_size", "country_code", "industry", "planned_use")
    CUSTOMER_NAME_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_SIZE_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_CODE_FIELD_NUMBER: _ClassVar[int]
    INDUSTRY_FIELD_NUMBER: _ClassVar[int]
    PLANNED_USE_FIELD_NUMBER: _ClassVar[int]
    customer_name: str
    organization_size: str
    country_code: str
    industry: str
    planned_use: TenantPlannedUse
    def __init__(self, customer_name: _Optional[str] = ..., organization_size: _Optional[str] = ..., country_code: _Optional[str] = ..., industry: _Optional[str] = ..., planned_use: _Optional[_Union[TenantPlannedUse, str]] = ...) -> None: ...

class NewUserInfo(_message.Message):
    __slots__ = ("email", "name", "password", "job_title", "marketing_opt_in", "terms_of_service_accepted", "utm_params")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    JOB_TITLE_FIELD_NUMBER: _ClassVar[int]
    MARKETING_OPT_IN_FIELD_NUMBER: _ClassVar[int]
    TERMS_OF_SERVICE_ACCEPTED_FIELD_NUMBER: _ClassVar[int]
    UTM_PARAMS_FIELD_NUMBER: _ClassVar[int]
    email: str
    name: str
    password: str
    job_title: str
    marketing_opt_in: bool
    terms_of_service_accepted: bool
    utm_params: UTMParams
    def __init__(self, email: _Optional[str] = ..., name: _Optional[str] = ..., password: _Optional[str] = ..., job_title: _Optional[str] = ..., marketing_opt_in: bool = ..., terms_of_service_accepted: bool = ..., utm_params: _Optional[_Union[UTMParams, _Mapping]] = ...) -> None: ...

class UTMParams(_message.Message):
    __slots__ = ("utm_campaign", "utm_source", "utm_medium")
    UTM_CAMPAIGN_FIELD_NUMBER: _ClassVar[int]
    UTM_SOURCE_FIELD_NUMBER: _ClassVar[int]
    UTM_MEDIUM_FIELD_NUMBER: _ClassVar[int]
    utm_campaign: str
    utm_source: str
    utm_medium: str
    def __init__(self, utm_campaign: _Optional[str] = ..., utm_source: _Optional[str] = ..., utm_medium: _Optional[str] = ...) -> None: ...

class RetriggerEmailVerificationRequest(_message.Message):
    __slots__ = ("email",)
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    email: str
    def __init__(self, email: _Optional[str] = ...) -> None: ...

class RetriggerEmailVerificationResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CreatedUserInfo(_message.Message):
    __slots__ = ("new_user_info", "new_user_id", "tenant_id", "access_token")
    NEW_USER_INFO_FIELD_NUMBER: _ClassVar[int]
    NEW_USER_ID_FIELD_NUMBER: _ClassVar[int]
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    new_user_info: NewUserInfo
    new_user_id: str
    tenant_id: str
    access_token: str
    def __init__(self, new_user_info: _Optional[_Union[NewUserInfo, _Mapping]] = ..., new_user_id: _Optional[str] = ..., tenant_id: _Optional[str] = ..., access_token: _Optional[str] = ...) -> None: ...

class ManualUpdateAwsSubscriptionEntitlementsRequest(_message.Message):
    __slots__ = ("tenant_id",)
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    tenant_id: str
    def __init__(self, tenant_id: _Optional[str] = ...) -> None: ...

class ManualUpdateAwsSubscriptionEntitlementsResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
