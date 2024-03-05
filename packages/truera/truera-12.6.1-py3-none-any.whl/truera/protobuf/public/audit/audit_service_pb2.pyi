from google.api import annotations_pb2 as _annotations_pb2
from truera.protobuf.public.util import time_range_pb2 as _time_range_pb2
from truera.protobuf.queryservice import query_service_pb2 as _query_service_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UserActivityType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN_USER_ACTIVITY: _ClassVar[UserActivityType]
    USER_LOGIN: _ClassVar[UserActivityType]
    ADD_PROJECT: _ClassVar[UserActivityType]
    DELETE_PROJECT: _ClassVar[UserActivityType]
    ADD_DATA_COLLECTION: _ClassVar[UserActivityType]
    DELETE_DATA_COLLECTION: _ClassVar[UserActivityType]
    ADD_DATA_SPLIT: _ClassVar[UserActivityType]
    DELETE_DATA_SPLIT: _ClassVar[UserActivityType]
    ADD_MODEL: _ClassVar[UserActivityType]
    DELETE_MODEL: _ClassVar[UserActivityType]
    ADD_DASHBOARD: _ClassVar[UserActivityType]
    DELETE_DASHBOARD: _ClassVar[UserActivityType]
    ADD_REPORT: _ClassVar[UserActivityType]
    DELETE_REPORT: _ClassVar[UserActivityType]

class UsageReportType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN_USAGE_REPORT: _ClassVar[UsageReportType]
    ACTIVE_USER_COUNT: _ClassVar[UsageReportType]
    TOTAL_LOGIN_COUNT: _ClassVar[UsageReportType]
    CREATE_PROJECT_COUNT: _ClassVar[UsageReportType]
    ACTIVE_USER_LIST: _ClassVar[UsageReportType]
UNKNOWN_USER_ACTIVITY: UserActivityType
USER_LOGIN: UserActivityType
ADD_PROJECT: UserActivityType
DELETE_PROJECT: UserActivityType
ADD_DATA_COLLECTION: UserActivityType
DELETE_DATA_COLLECTION: UserActivityType
ADD_DATA_SPLIT: UserActivityType
DELETE_DATA_SPLIT: UserActivityType
ADD_MODEL: UserActivityType
DELETE_MODEL: UserActivityType
ADD_DASHBOARD: UserActivityType
DELETE_DASHBOARD: UserActivityType
ADD_REPORT: UserActivityType
DELETE_REPORT: UserActivityType
UNKNOWN_USAGE_REPORT: UsageReportType
ACTIVE_USER_COUNT: UsageReportType
TOTAL_LOGIN_COUNT: UsageReportType
CREATE_PROJECT_COUNT: UsageReportType
ACTIVE_USER_LIST: UsageReportType

class AuditPingRequest(_message.Message):
    __slots__ = ("ping_string",)
    PING_STRING_FIELD_NUMBER: _ClassVar[int]
    ping_string: str
    def __init__(self, ping_string: _Optional[str] = ...) -> None: ...

class AuditPingResponse(_message.Message):
    __slots__ = ("ping_response",)
    PING_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    ping_response: str
    def __init__(self, ping_response: _Optional[str] = ...) -> None: ...

class CreateUserActivityReportRequest(_message.Message):
    __slots__ = ("tenant_id", "user_id", "time_window", "user_activity_type", "workspace_id")
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    TIME_WINDOW_FIELD_NUMBER: _ClassVar[int]
    USER_ACTIVITY_TYPE_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    tenant_id: str
    user_id: str
    time_window: _time_range_pb2.TimeRange
    user_activity_type: _containers.RepeatedScalarFieldContainer[UserActivityType]
    workspace_id: str
    def __init__(self, tenant_id: _Optional[str] = ..., user_id: _Optional[str] = ..., time_window: _Optional[_Union[_time_range_pb2.TimeRange, _Mapping]] = ..., user_activity_type: _Optional[_Iterable[_Union[UserActivityType, str]]] = ..., workspace_id: _Optional[str] = ...) -> None: ...

class CreateUserActivityReportResponse(_message.Message):
    __slots__ = ("records",)
    RECORDS_FIELD_NUMBER: _ClassVar[int]
    records: _query_service_pb2.RowMajorValueTable
    def __init__(self, records: _Optional[_Union[_query_service_pb2.RowMajorValueTable, _Mapping]] = ...) -> None: ...

class CreateUsageReportRequest(_message.Message):
    __slots__ = ("tenant_id", "time_window", "usage_report_type", "workspace_id")
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    TIME_WINDOW_FIELD_NUMBER: _ClassVar[int]
    USAGE_REPORT_TYPE_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    tenant_id: str
    time_window: _time_range_pb2.TimeRange
    usage_report_type: UsageReportType
    workspace_id: str
    def __init__(self, tenant_id: _Optional[str] = ..., time_window: _Optional[_Union[_time_range_pb2.TimeRange, _Mapping]] = ..., usage_report_type: _Optional[_Union[UsageReportType, str]] = ..., workspace_id: _Optional[str] = ...) -> None: ...

class CreateUsageReportResponse(_message.Message):
    __slots__ = ("records",)
    RECORDS_FIELD_NUMBER: _ClassVar[int]
    records: _query_service_pb2.RowMajorValueTable
    def __init__(self, records: _Optional[_Union[_query_service_pb2.RowMajorValueTable, _Mapping]] = ...) -> None: ...

class CreateUserActivityUberReportRequest(_message.Message):
    __slots__ = ("tenant_id", "time_window", "user_ids", "workspace_id")
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    TIME_WINDOW_FIELD_NUMBER: _ClassVar[int]
    USER_IDS_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    tenant_id: str
    time_window: _time_range_pb2.TimeRange
    user_ids: _containers.RepeatedScalarFieldContainer[str]
    workspace_id: str
    def __init__(self, tenant_id: _Optional[str] = ..., time_window: _Optional[_Union[_time_range_pb2.TimeRange, _Mapping]] = ..., user_ids: _Optional[_Iterable[str]] = ..., workspace_id: _Optional[str] = ...) -> None: ...

class CreateUserActivityUberReportResponse(_message.Message):
    __slots__ = ("records",)
    RECORDS_FIELD_NUMBER: _ClassVar[int]
    records: _query_service_pb2.RowMajorValueTable
    def __init__(self, records: _Optional[_Union[_query_service_pb2.RowMajorValueTable, _Mapping]] = ...) -> None: ...
