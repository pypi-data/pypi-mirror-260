from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.api import visibility_pb2 as _visibility_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from truera.protobuf.public import truera_custom_options_pb2 as _truera_custom_options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Privilege(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PV_NONE: _ClassVar[Privilege]
    PV_ALL: _ClassVar[Privilege]
    PV_CREATE: _ClassVar[Privilege]
    PV_VIEW: _ClassVar[Privilege]
    PV_MODIFY: _ClassVar[Privilege]
    PV_DELETE: _ClassVar[Privilege]
    PV_MEMBER: _ClassVar[Privilege]
    PV_GRANT_ROLE: _ClassVar[Privilege]
    PV_REVOKE_ROLE: _ClassVar[Privilege]
    PV_ADD_USER: _ClassVar[Privilege]
    PV_REMOVE_USER: _ClassVar[Privilege]
    PV_TRANSFER_OWNER: _ClassVar[Privilege]
    PV_VIEW_USERS: _ClassVar[Privilege]
    PV_VIEW_PROJECT: _ClassVar[Privilege]
    PV_CREATE_PROJECT: _ClassVar[Privilege]
    PV_ARCHIVE_PROJECT: _ClassVar[Privilege]
    PV_UPLOAD_DATA: _ClassVar[Privilege]
    PV_ANALYZE_PROJECT: _ClassVar[Privilege]
    PV_DELETE_PROJECT: _ClassVar[Privilege]
    PV_MODIFY_PROJECT: _ClassVar[Privilege]
    PV_VIEW_JOBS: _ClassVar[Privilege]
    PV_CREATE_JOBS: _ClassVar[Privilege]
    PV_DELETE_JOBS: _ClassVar[Privilege]
    PV_CLONE_MODEL: _ClassVar[Privilege]
    PV_PROVISION_TENANT: _ClassVar[Privilege]
    PV_INVITE_USER_TO_TENANT: _ClassVar[Privilege]
    PV_CREATE_DASHBOARD: _ClassVar[Privilege]
    PV_VIEW_DASHBOARD: _ClassVar[Privilege]

class ResourceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RT_NONE: _ClassVar[ResourceType]
    RT_ANY: _ClassVar[ResourceType]
    RT_RBAC: _ClassVar[ResourceType]
    RT_PROJECT: _ClassVar[ResourceType]
    RT_GROUP: _ClassVar[ResourceType]
    RT_WORKSPACE: _ClassVar[ResourceType]
    RT_DASHBOARD: _ClassVar[ResourceType]

class ActorType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AT_USER: _ClassVar[ActorType]
    AT_GROUP: _ClassVar[ActorType]

class GroupType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GT_NATIVE: _ClassVar[GroupType]
    GT_SYNCED: _ClassVar[GroupType]

class RoleType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RLT_DIRECT: _ClassVar[RoleType]
    RLT_INHERITED: _ClassVar[RoleType]
PV_NONE: Privilege
PV_ALL: Privilege
PV_CREATE: Privilege
PV_VIEW: Privilege
PV_MODIFY: Privilege
PV_DELETE: Privilege
PV_MEMBER: Privilege
PV_GRANT_ROLE: Privilege
PV_REVOKE_ROLE: Privilege
PV_ADD_USER: Privilege
PV_REMOVE_USER: Privilege
PV_TRANSFER_OWNER: Privilege
PV_VIEW_USERS: Privilege
PV_VIEW_PROJECT: Privilege
PV_CREATE_PROJECT: Privilege
PV_ARCHIVE_PROJECT: Privilege
PV_UPLOAD_DATA: Privilege
PV_ANALYZE_PROJECT: Privilege
PV_DELETE_PROJECT: Privilege
PV_MODIFY_PROJECT: Privilege
PV_VIEW_JOBS: Privilege
PV_CREATE_JOBS: Privilege
PV_DELETE_JOBS: Privilege
PV_CLONE_MODEL: Privilege
PV_PROVISION_TENANT: Privilege
PV_INVITE_USER_TO_TENANT: Privilege
PV_CREATE_DASHBOARD: Privilege
PV_VIEW_DASHBOARD: Privilege
RT_NONE: ResourceType
RT_ANY: ResourceType
RT_RBAC: ResourceType
RT_PROJECT: ResourceType
RT_GROUP: ResourceType
RT_WORKSPACE: ResourceType
RT_DASHBOARD: ResourceType
AT_USER: ActorType
AT_GROUP: ActorType
GT_NATIVE: GroupType
GT_SYNCED: GroupType
RLT_DIRECT: RoleType
RLT_INHERITED: RoleType

class ClientCreateTenantRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ClientListTenantsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListTenantsForDeploymentRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ClientListTenantsResponse(_message.Message):
    __slots__ = ("tenants",)
    TENANTS_FIELD_NUMBER: _ClassVar[int]
    tenants: _containers.RepeatedCompositeFieldContainer[ClientTenantInfo]
    def __init__(self, tenants: _Optional[_Iterable[_Union[ClientTenantInfo, _Mapping]]] = ...) -> None: ...

class ClientTenantInfo(_message.Message):
    __slots__ = ("tenant_id",)
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    tenant_id: str
    def __init__(self, tenant_id: _Optional[str] = ...) -> None: ...

class RbacPingRequest(_message.Message):
    __slots__ = ("ping_string",)
    PING_STRING_FIELD_NUMBER: _ClassVar[int]
    ping_string: str
    def __init__(self, ping_string: _Optional[str] = ...) -> None: ...

class RbacPingResponse(_message.Message):
    __slots__ = ("ping_response",)
    PING_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    ping_response: str
    def __init__(self, ping_response: _Optional[str] = ...) -> None: ...

class CheckPermissionRequest(_message.Message):
    __slots__ = ("user_id", "privileges", "resource_id")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    PRIVILEGES_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    privileges: _containers.RepeatedScalarFieldContainer[Privilege]
    resource_id: ResourceId
    def __init__(self, user_id: _Optional[str] = ..., privileges: _Optional[_Iterable[_Union[Privilege, str]]] = ..., resource_id: _Optional[_Union[ResourceId, _Mapping]] = ...) -> None: ...

class BatchCheckPermissionsRequest(_message.Message):
    __slots__ = ("user_id", "permission_checks")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    PERMISSION_CHECKS_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    permission_checks: _containers.RepeatedCompositeFieldContainer[PermissionsCheck]
    def __init__(self, user_id: _Optional[str] = ..., permission_checks: _Optional[_Iterable[_Union[PermissionsCheck, _Mapping]]] = ...) -> None: ...

class PermissionsCheck(_message.Message):
    __slots__ = ("privileges", "resource_id")
    PRIVILEGES_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    privileges: _containers.RepeatedScalarFieldContainer[Privilege]
    resource_id: ResourceId
    def __init__(self, privileges: _Optional[_Iterable[_Union[Privilege, str]]] = ..., resource_id: _Optional[_Union[ResourceId, _Mapping]] = ...) -> None: ...

class PermissionsCheckResponse(_message.Message):
    __slots__ = ("response", "permission_check")
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    PERMISSION_CHECK_FIELD_NUMBER: _ClassVar[int]
    response: AuthorizationResponse
    permission_check: PermissionsCheck
    def __init__(self, response: _Optional[_Union[AuthorizationResponse, _Mapping]] = ..., permission_check: _Optional[_Union[PermissionsCheck, _Mapping]] = ...) -> None: ...

class BatchCheckPermissionsResponse(_message.Message):
    __slots__ = ("response", "check_permission_responses")
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    CHECK_PERMISSION_RESPONSES_FIELD_NUMBER: _ClassVar[int]
    response: AuthorizationResponse
    check_permission_responses: _containers.RepeatedCompositeFieldContainer[PermissionsCheckResponse]
    def __init__(self, response: _Optional[_Union[AuthorizationResponse, _Mapping]] = ..., check_permission_responses: _Optional[_Iterable[_Union[PermissionsCheckResponse, _Mapping]]] = ...) -> None: ...

class RoleRequest(_message.Message):
    __slots__ = ("requestor_user_id", "role_id", "subject_id", "resource_id")
    REQUESTOR_USER_ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    requestor_user_id: str
    role_id: str
    subject_id: str
    resource_id: ResourceId
    def __init__(self, requestor_user_id: _Optional[str] = ..., role_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., resource_id: _Optional[_Union[ResourceId, _Mapping]] = ...) -> None: ...

class AuthorizationResponse(_message.Message):
    __slots__ = ("status", "denial_reason")
    class AuthStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[AuthorizationResponse.AuthStatus]
        INTERNAL_ERROR: _ClassVar[AuthorizationResponse.AuthStatus]
        GRANTED: _ClassVar[AuthorizationResponse.AuthStatus]
        DENIED: _ClassVar[AuthorizationResponse.AuthStatus]
    UNKNOWN: AuthorizationResponse.AuthStatus
    INTERNAL_ERROR: AuthorizationResponse.AuthStatus
    GRANTED: AuthorizationResponse.AuthStatus
    DENIED: AuthorizationResponse.AuthStatus
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DENIAL_REASON_FIELD_NUMBER: _ClassVar[int]
    status: AuthorizationResponse.AuthStatus
    denial_reason: str
    def __init__(self, status: _Optional[_Union[AuthorizationResponse.AuthStatus, str]] = ..., denial_reason: _Optional[str] = ...) -> None: ...

class AdminRequest(_message.Message):
    __slots__ = ("requestor_user_id", "subject_id")
    REQUESTOR_USER_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    requestor_user_id: str
    subject_id: str
    def __init__(self, requestor_user_id: _Optional[str] = ..., subject_id: _Optional[str] = ...) -> None: ...

class ProvisionTenantRequest(_message.Message):
    __slots__ = ("requestor_user_id", "user", "user_tenant_info")
    REQUESTOR_USER_ID_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    USER_TENANT_INFO_FIELD_NUMBER: _ClassVar[int]
    requestor_user_id: str
    user: User
    user_tenant_info: UserTenantInfo
    def __init__(self, requestor_user_id: _Optional[str] = ..., user: _Optional[_Union[User, _Mapping]] = ..., user_tenant_info: _Optional[_Union[UserTenantInfo, _Mapping]] = ...) -> None: ...

class ProvisionTenantResponse(_message.Message):
    __slots__ = ("token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...

class PromoteStagedUserRequest(_message.Message):
    __slots__ = ("requestor_user_id", "subject_id")
    REQUESTOR_USER_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    requestor_user_id: str
    subject_id: str
    def __init__(self, requestor_user_id: _Optional[str] = ..., subject_id: _Optional[str] = ...) -> None: ...

class DemoteUserRequest(_message.Message):
    __slots__ = ("requestor_user_id", "subject_id")
    REQUESTOR_USER_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    requestor_user_id: str
    subject_id: str
    def __init__(self, requestor_user_id: _Optional[str] = ..., subject_id: _Optional[str] = ...) -> None: ...

class PermissionsRequest(_message.Message):
    __slots__ = ("requestor_user_id", "user_id", "resource_id", "workspace_id")
    REQUESTOR_USER_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    requestor_user_id: str
    user_id: str
    resource_id: ResourceId
    workspace_id: str
    def __init__(self, requestor_user_id: _Optional[str] = ..., user_id: _Optional[str] = ..., resource_id: _Optional[_Union[ResourceId, _Mapping]] = ..., workspace_id: _Optional[str] = ...) -> None: ...

class PermissionsResponse(_message.Message):
    __slots__ = ("permissions",)
    class UserPermission(_message.Message):
        __slots__ = ("user_id", "privilege", "resource_id")
        USER_ID_FIELD_NUMBER: _ClassVar[int]
        PRIVILEGE_FIELD_NUMBER: _ClassVar[int]
        RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
        user_id: str
        privilege: Privilege
        resource_id: ResourceId
        def __init__(self, user_id: _Optional[str] = ..., privilege: _Optional[_Union[Privilege, str]] = ..., resource_id: _Optional[_Union[ResourceId, _Mapping]] = ...) -> None: ...
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    permissions: _containers.RepeatedCompositeFieldContainer[PermissionsResponse.UserPermission]
    def __init__(self, permissions: _Optional[_Iterable[_Union[PermissionsResponse.UserPermission, _Mapping]]] = ...) -> None: ...

class GetResourceFilter(_message.Message):
    __slots__ = ("user_id", "privileges", "resource_types", "workspace_id")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    PRIVILEGES_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_TYPES_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    privileges: _containers.RepeatedScalarFieldContainer[Privilege]
    resource_types: _containers.RepeatedScalarFieldContainer[ResourceType]
    workspace_id: str
    def __init__(self, user_id: _Optional[str] = ..., privileges: _Optional[_Iterable[_Union[Privilege, str]]] = ..., resource_types: _Optional[_Iterable[_Union[ResourceType, str]]] = ..., workspace_id: _Optional[str] = ...) -> None: ...

class GetResourceResponse(_message.Message):
    __slots__ = ("resource_id",)
    RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    resource_id: _containers.RepeatedCompositeFieldContainer[ResourceId]
    def __init__(self, resource_id: _Optional[_Iterable[_Union[ResourceId, _Mapping]]] = ...) -> None: ...

class GetRolesRequest(_message.Message):
    __slots__ = ("user_id", "resource_id", "requestor_user_id", "workspace_id", "resource_type")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    REQUESTOR_USER_ID_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    resource_id: ResourceId
    requestor_user_id: str
    workspace_id: str
    resource_type: ResourceType
    def __init__(self, user_id: _Optional[str] = ..., resource_id: _Optional[_Union[ResourceId, _Mapping]] = ..., requestor_user_id: _Optional[str] = ..., workspace_id: _Optional[str] = ..., resource_type: _Optional[_Union[ResourceType, str]] = ...) -> None: ...

class GetRolesResponse(_message.Message):
    __slots__ = ("roles",)
    class UserRole(_message.Message):
        __slots__ = ("user_id", "role_id", "resource_id", "actor_type", "role_type")
        USER_ID_FIELD_NUMBER: _ClassVar[int]
        ROLE_ID_FIELD_NUMBER: _ClassVar[int]
        RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
        ACTOR_TYPE_FIELD_NUMBER: _ClassVar[int]
        ROLE_TYPE_FIELD_NUMBER: _ClassVar[int]
        user_id: str
        role_id: str
        resource_id: ResourceId
        actor_type: ActorType
        role_type: RoleType
        def __init__(self, user_id: _Optional[str] = ..., role_id: _Optional[str] = ..., resource_id: _Optional[_Union[ResourceId, _Mapping]] = ..., actor_type: _Optional[_Union[ActorType, str]] = ..., role_type: _Optional[_Union[RoleType, str]] = ...) -> None: ...
    ROLES_FIELD_NUMBER: _ClassVar[int]
    roles: _containers.RepeatedCompositeFieldContainer[GetRolesResponse.UserRole]
    def __init__(self, roles: _Optional[_Iterable[_Union[GetRolesResponse.UserRole, _Mapping]]] = ...) -> None: ...

class AddUserRequest(_message.Message):
    __slots__ = ("requestor_user_id", "user")
    REQUESTOR_USER_ID_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    requestor_user_id: str
    user: User
    def __init__(self, requestor_user_id: _Optional[str] = ..., user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class AutoUserRequest(_message.Message):
    __slots__ = ("requestor_user_id",)
    REQUESTOR_USER_ID_FIELD_NUMBER: _ClassVar[int]
    requestor_user_id: str
    def __init__(self, requestor_user_id: _Optional[str] = ...) -> None: ...

class InviteUserRequest(_message.Message):
    __slots__ = ("requestor_user_id", "user", "tenant_id")
    REQUESTOR_USER_ID_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    requestor_user_id: str
    user: User
    tenant_id: str
    def __init__(self, requestor_user_id: _Optional[str] = ..., user: _Optional[_Union[User, _Mapping]] = ..., tenant_id: _Optional[str] = ...) -> None: ...

class GetUsersFilter(_message.Message):
    __slots__ = ("contains", "include_service_accounts", "requestor_user_id", "workspace_id")
    CONTAINS_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_SERVICE_ACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    REQUESTOR_USER_ID_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    contains: _containers.RepeatedScalarFieldContainer[str]
    include_service_accounts: bool
    requestor_user_id: str
    workspace_id: str
    def __init__(self, contains: _Optional[_Iterable[str]] = ..., include_service_accounts: bool = ..., requestor_user_id: _Optional[str] = ..., workspace_id: _Optional[str] = ...) -> None: ...

class GetUsersResponse(_message.Message):
    __slots__ = ("users",)
    USERS_FIELD_NUMBER: _ClassVar[int]
    users: _containers.RepeatedCompositeFieldContainer[User]
    def __init__(self, users: _Optional[_Iterable[_Union[User, _Mapping]]] = ...) -> None: ...

class GetCurrentUserResponse(_message.Message):
    __slots__ = ("current_user", "tenant_id")
    CURRENT_USER_FIELD_NUMBER: _ClassVar[int]
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    current_user: User
    tenant_id: str
    def __init__(self, current_user: _Optional[_Union[User, _Mapping]] = ..., tenant_id: _Optional[str] = ...) -> None: ...

class UserProjectRequest(_message.Message):
    __slots__ = ("requestor_user_id", "subject_id", "project_id", "as_owner")
    REQUESTOR_USER_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    AS_OWNER_FIELD_NUMBER: _ClassVar[int]
    requestor_user_id: str
    subject_id: str
    project_id: str
    as_owner: bool
    def __init__(self, requestor_user_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., project_id: _Optional[str] = ..., as_owner: bool = ...) -> None: ...

class ProjectRequest(_message.Message):
    __slots__ = ("requestor_user_id", "project_id")
    REQUESTOR_USER_ID_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    requestor_user_id: str
    project_id: str
    def __init__(self, requestor_user_id: _Optional[str] = ..., project_id: _Optional[str] = ...) -> None: ...

class CreateServiceAccountRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class RefreshServiceAccountCredentialsRequest(_message.Message):
    __slots__ = ("client_id",)
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    def __init__(self, client_id: _Optional[str] = ...) -> None: ...

class DeleteServiceAccountRequest(_message.Message):
    __slots__ = ("client_id",)
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    def __init__(self, client_id: _Optional[str] = ...) -> None: ...

class GetServiceAccountsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class AuthorizeResourceRequest(_message.Message):
    __slots__ = ("requestor_user_id", "resource_id", "workspace_id")
    REQUESTOR_USER_ID_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    requestor_user_id: str
    resource_id: ResourceId
    workspace_id: str
    def __init__(self, requestor_user_id: _Optional[str] = ..., resource_id: _Optional[_Union[ResourceId, _Mapping]] = ..., workspace_id: _Optional[str] = ...) -> None: ...

class SubjectResourceRequest(_message.Message):
    __slots__ = ("requestor_user_id", "resource_id", "subject_id")
    REQUESTOR_USER_ID_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    requestor_user_id: str
    resource_id: ResourceId
    subject_id: str
    def __init__(self, requestor_user_id: _Optional[str] = ..., resource_id: _Optional[_Union[ResourceId, _Mapping]] = ..., subject_id: _Optional[str] = ...) -> None: ...

class ServiceAccountCredentials(_message.Message):
    __slots__ = ("client_id", "client_secret")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    client_secret: str
    def __init__(self, client_id: _Optional[str] = ..., client_secret: _Optional[str] = ...) -> None: ...

class CreateGroupRequest(_message.Message):
    __slots__ = ("requestor_user_id", "name", "email", "description", "external_sync_id", "group_type")
    REQUESTOR_USER_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_SYNC_ID_FIELD_NUMBER: _ClassVar[int]
    GROUP_TYPE_FIELD_NUMBER: _ClassVar[int]
    requestor_user_id: str
    name: str
    email: str
    description: str
    external_sync_id: str
    group_type: GroupType
    def __init__(self, requestor_user_id: _Optional[str] = ..., name: _Optional[str] = ..., email: _Optional[str] = ..., description: _Optional[str] = ..., external_sync_id: _Optional[str] = ..., group_type: _Optional[_Union[GroupType, str]] = ...) -> None: ...

class UpdateGroupRequest(_message.Message):
    __slots__ = ("requestor_user_id", "group_id", "name", "description")
    REQUESTOR_USER_ID_FIELD_NUMBER: _ClassVar[int]
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    requestor_user_id: str
    group_id: str
    name: str
    description: str
    def __init__(self, requestor_user_id: _Optional[str] = ..., group_id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class CreateGroupResponse(_message.Message):
    __slots__ = ("name", "group_id")
    NAME_FIELD_NUMBER: _ClassVar[int]
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    group_id: str
    def __init__(self, name: _Optional[str] = ..., group_id: _Optional[str] = ...) -> None: ...

class GroupRequest(_message.Message):
    __slots__ = ("requestor_user_id", "group_id")
    REQUESTOR_USER_ID_FIELD_NUMBER: _ClassVar[int]
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    requestor_user_id: str
    group_id: str
    def __init__(self, requestor_user_id: _Optional[str] = ..., group_id: _Optional[str] = ...) -> None: ...

class GroupInfoResponse(_message.Message):
    __slots__ = ("group_id", "name", "email", "description", "external_sync_id", "group_type", "users")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_SYNC_ID_FIELD_NUMBER: _ClassVar[int]
    GROUP_TYPE_FIELD_NUMBER: _ClassVar[int]
    USERS_FIELD_NUMBER: _ClassVar[int]
    group_id: str
    name: str
    email: str
    description: str
    external_sync_id: str
    group_type: GroupType
    users: _containers.RepeatedCompositeFieldContainer[User]
    def __init__(self, group_id: _Optional[str] = ..., name: _Optional[str] = ..., email: _Optional[str] = ..., description: _Optional[str] = ..., external_sync_id: _Optional[str] = ..., group_type: _Optional[_Union[GroupType, str]] = ..., users: _Optional[_Iterable[_Union[User, _Mapping]]] = ...) -> None: ...

class GroupUsersRequest(_message.Message):
    __slots__ = ("requestor_user_id", "group_id", "user_ids")
    REQUESTOR_USER_ID_FIELD_NUMBER: _ClassVar[int]
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    USER_IDS_FIELD_NUMBER: _ClassVar[int]
    requestor_user_id: str
    group_id: str
    user_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, requestor_user_id: _Optional[str] = ..., group_id: _Optional[str] = ..., user_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class GetGroupsRequest(_message.Message):
    __slots__ = ("user_id", "requestor_user_id", "workspace_id")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    REQUESTOR_USER_ID_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    requestor_user_id: str
    workspace_id: str
    def __init__(self, user_id: _Optional[str] = ..., requestor_user_id: _Optional[str] = ..., workspace_id: _Optional[str] = ...) -> None: ...

class GetGroupsResponse(_message.Message):
    __slots__ = ("groups_info",)
    class GroupListInfo(_message.Message):
        __slots__ = ("group", "num_members", "users")
        GROUP_FIELD_NUMBER: _ClassVar[int]
        NUM_MEMBERS_FIELD_NUMBER: _ClassVar[int]
        USERS_FIELD_NUMBER: _ClassVar[int]
        group: Group
        num_members: int
        users: _containers.RepeatedCompositeFieldContainer[User]
        def __init__(self, group: _Optional[_Union[Group, _Mapping]] = ..., num_members: _Optional[int] = ..., users: _Optional[_Iterable[_Union[User, _Mapping]]] = ...) -> None: ...
    GROUPS_INFO_FIELD_NUMBER: _ClassVar[int]
    groups_info: _containers.RepeatedCompositeFieldContainer[GetGroupsResponse.GroupListInfo]
    def __init__(self, groups_info: _Optional[_Iterable[_Union[GetGroupsResponse.GroupListInfo, _Mapping]]] = ...) -> None: ...

class GetCurrentTenantInfoRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetCurrentTenantInfoResponse(_message.Message):
    __slots__ = ("user_tenant_info",)
    USER_TENANT_INFO_FIELD_NUMBER: _ClassVar[int]
    user_tenant_info: UserTenantInfo
    def __init__(self, user_tenant_info: _Optional[_Union[UserTenantInfo, _Mapping]] = ...) -> None: ...

class CreateWorkspaceRequest(_message.Message):
    __slots__ = ("name", "description")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class CreateWorkspaceResponse(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class UpdateWorkspaceRequest(_message.Message):
    __slots__ = ("workspace_id", "name", "description")
    WORKSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    workspace_id: str
    name: str
    description: str
    def __init__(self, workspace_id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class UpdateAttributeForResourceRequest(_message.Message):
    __slots__ = ("resource_id", "workspace_id")
    RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    resource_id: ResourceId
    workspace_id: str
    def __init__(self, resource_id: _Optional[_Union[ResourceId, _Mapping]] = ..., workspace_id: _Optional[str] = ...) -> None: ...

class UpdateAttributeForResourceResponse(_message.Message):
    __slots__ = ("workspace_id",)
    WORKSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    workspace_id: str
    def __init__(self, workspace_id: _Optional[str] = ...) -> None: ...

class GetWorkspaceInfoRequest(_message.Message):
    __slots__ = ("workspace_id", "name", "resource_id")
    WORKSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    workspace_id: str
    name: str
    resource_id: ResourceId
    def __init__(self, workspace_id: _Optional[str] = ..., name: _Optional[str] = ..., resource_id: _Optional[_Union[ResourceId, _Mapping]] = ...) -> None: ...

class WorkspaceInfoResponse(_message.Message):
    __slots__ = ("workspace_id", "name", "description")
    WORKSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    workspace_id: str
    name: str
    description: str
    def __init__(self, workspace_id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class GetWorkspacesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetWorkspacesResponse(_message.Message):
    __slots__ = ("workspaces",)
    WORKSPACES_FIELD_NUMBER: _ClassVar[int]
    workspaces: _containers.RepeatedCompositeFieldContainer[WorkspaceInfoResponse]
    def __init__(self, workspaces: _Optional[_Iterable[_Union[WorkspaceInfoResponse, _Mapping]]] = ...) -> None: ...

class GrantBatchResourceRolesRequest(_message.Message):
    __slots__ = ("roles",)
    ROLES_FIELD_NUMBER: _ClassVar[int]
    roles: _containers.RepeatedCompositeFieldContainer[RoleRequest]
    def __init__(self, roles: _Optional[_Iterable[_Union[RoleRequest, _Mapping]]] = ...) -> None: ...

class BatchGrantRoleResponse(_message.Message):
    __slots__ = ("role", "response")
    ROLE_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    role: RoleRequest
    response: AuthorizationResponse
    def __init__(self, role: _Optional[_Union[RoleRequest, _Mapping]] = ..., response: _Optional[_Union[AuthorizationResponse, _Mapping]] = ...) -> None: ...

class GrantBatchResourceRolesResponse(_message.Message):
    __slots__ = ("response", "grant_role_responses")
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    GRANT_ROLE_RESPONSES_FIELD_NUMBER: _ClassVar[int]
    response: AuthorizationResponse
    grant_role_responses: _containers.RepeatedCompositeFieldContainer[BatchGrantRoleResponse]
    def __init__(self, response: _Optional[_Union[AuthorizationResponse, _Mapping]] = ..., grant_role_responses: _Optional[_Iterable[_Union[BatchGrantRoleResponse, _Mapping]]] = ...) -> None: ...

class ResourceId(_message.Message):
    __slots__ = ("resource_type", "resource_id")
    RESOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    resource_type: ResourceType
    resource_id: str
    def __init__(self, resource_type: _Optional[_Union[ResourceType, str]] = ..., resource_id: _Optional[str] = ...) -> None: ...

class Role(_message.Message):
    __slots__ = ("id", "description")
    ID_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    id: str
    description: str
    def __init__(self, id: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class Permission(_message.Message):
    __slots__ = ("id", "name", "description", "role_id", "privileges")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ROLE_ID_FIELD_NUMBER: _ClassVar[int]
    PRIVILEGES_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    role_id: str
    privileges: _containers.RepeatedScalarFieldContainer[Privilege]
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., role_id: _Optional[str] = ..., privileges: _Optional[_Iterable[_Union[Privilege, str]]] = ...) -> None: ...

class Subject(_message.Message):
    __slots__ = ("id", "name", "role_ids", "actor_type", "info")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ROLE_IDS_FIELD_NUMBER: _ClassVar[int]
    ACTOR_TYPE_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    role_ids: _containers.RepeatedScalarFieldContainer[str]
    actor_type: ActorType
    info: _struct_pb2.Struct
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., role_ids: _Optional[_Iterable[str]] = ..., actor_type: _Optional[_Union[ActorType, str]] = ..., info: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class User(_message.Message):
    __slots__ = ("id", "name", "email", "subject_ids", "group_ids", "has_init_workspace_roles", "user_info", "meta_info")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_IDS_FIELD_NUMBER: _ClassVar[int]
    GROUP_IDS_FIELD_NUMBER: _ClassVar[int]
    HAS_INIT_WORKSPACE_ROLES_FIELD_NUMBER: _ClassVar[int]
    USER_INFO_FIELD_NUMBER: _ClassVar[int]
    META_INFO_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    email: str
    subject_ids: _containers.RepeatedScalarFieldContainer[str]
    group_ids: _containers.RepeatedScalarFieldContainer[str]
    has_init_workspace_roles: bool
    user_info: _struct_pb2.Struct
    meta_info: MetaUserInfo
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., email: _Optional[str] = ..., subject_ids: _Optional[_Iterable[str]] = ..., group_ids: _Optional[_Iterable[str]] = ..., has_init_workspace_roles: bool = ..., user_info: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., meta_info: _Optional[_Union[MetaUserInfo, _Mapping]] = ...) -> None: ...

class MetaUserInfo(_message.Message):
    __slots__ = ("tos_accepted", "is_service_account", "client_id")
    TOS_ACCEPTED_FIELD_NUMBER: _ClassVar[int]
    IS_SERVICE_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    tos_accepted: bool
    is_service_account: bool
    client_id: str
    def __init__(self, tos_accepted: bool = ..., is_service_account: bool = ..., client_id: _Optional[str] = ...) -> None: ...

class Resource(_message.Message):
    __slots__ = ("id", "subject_roles", "workspace_id")
    class SubjectRole(_message.Message):
        __slots__ = ("subject_id", "role_id")
        SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
        ROLE_ID_FIELD_NUMBER: _ClassVar[int]
        subject_id: str
        role_id: str
        def __init__(self, subject_id: _Optional[str] = ..., role_id: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ROLES_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    subject_roles: _containers.RepeatedCompositeFieldContainer[Resource.SubjectRole]
    workspace_id: str
    def __init__(self, id: _Optional[str] = ..., subject_roles: _Optional[_Iterable[_Union[Resource.SubjectRole, _Mapping]]] = ..., workspace_id: _Optional[str] = ...) -> None: ...

class Group(_message.Message):
    __slots__ = ("id", "creator_user_id", "name", "email", "subject_id", "description", "external_sync_id", "group_type")
    ID_FIELD_NUMBER: _ClassVar[int]
    CREATOR_USER_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_SYNC_ID_FIELD_NUMBER: _ClassVar[int]
    GROUP_TYPE_FIELD_NUMBER: _ClassVar[int]
    id: str
    creator_user_id: str
    name: str
    email: str
    subject_id: str
    description: str
    external_sync_id: str
    group_type: GroupType
    def __init__(self, id: _Optional[str] = ..., creator_user_id: _Optional[str] = ..., name: _Optional[str] = ..., email: _Optional[str] = ..., subject_id: _Optional[str] = ..., description: _Optional[str] = ..., external_sync_id: _Optional[str] = ..., group_type: _Optional[_Union[GroupType, str]] = ...) -> None: ...

class UserTenantInfo(_message.Message):
    __slots__ = ("id", "user_tenant_id", "user_tenant_name")
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    USER_TENANT_NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    user_tenant_id: str
    user_tenant_name: str
    def __init__(self, id: _Optional[str] = ..., user_tenant_id: _Optional[str] = ..., user_tenant_name: _Optional[str] = ...) -> None: ...

class Workspace(_message.Message):
    __slots__ = ("id", "creator_user_id", "name", "description")
    ID_FIELD_NUMBER: _ClassVar[int]
    CREATOR_USER_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    id: str
    creator_user_id: str
    name: str
    description: str
    def __init__(self, id: _Optional[str] = ..., creator_user_id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...
