from google.api import annotations_pb2 as _annotations_pb2
from google.api import visibility_pb2 as _visibility_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from truera.protobuf.public import truera_custom_options_pb2 as _truera_custom_options_pb2
from truera.protobuf.public.data_service import data_service_pb2 as _data_service_pb2
from truera.protobuf.public.util import time_range_pb2 as _time_range_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CronElementType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TDK_INVALID: _ClassVar[CronElementType]
    TDK_MINUTE_OF_HOUR: _ClassVar[CronElementType]
    TDK_HOUR_OF_DAY: _ClassVar[CronElementType]
    TDK_DAY_OF_MONTH: _ClassVar[CronElementType]
    TDK_MONTH_OF_YEAR: _ClassVar[CronElementType]
    TDK_DAY_OF_WEEK: _ClassVar[CronElementType]
TDK_INVALID: CronElementType
TDK_MINUTE_OF_HOUR: CronElementType
TDK_HOUR_OF_DAY: CronElementType
TDK_DAY_OF_MONTH: CronElementType
TDK_MONTH_OF_YEAR: CronElementType
TDK_DAY_OF_WEEK: CronElementType

class ScheduleIngestionRequest(_message.Message):
    __slots__ = ("request_template", "schedule", "historical_start_time")
    REQUEST_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    HISTORICAL_START_TIME_FIELD_NUMBER: _ClassVar[int]
    request_template: DataServiceRequestTree
    schedule: Schedule
    historical_start_time: _timestamp_pb2.Timestamp
    def __init__(self, request_template: _Optional[_Union[DataServiceRequestTree, _Mapping]] = ..., schedule: _Optional[_Union[Schedule, _Mapping]] = ..., historical_start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class DataServiceRequestTree(_message.Message):
    __slots__ = ("load_req", "filter", "join", "materialize", "parents")
    LOAD_REQ_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    JOIN_FIELD_NUMBER: _ClassVar[int]
    MATERIALIZE_FIELD_NUMBER: _ClassVar[int]
    PARENTS_FIELD_NUMBER: _ClassVar[int]
    load_req: _data_service_pb2.LoadDataRequest
    filter: _data_service_pb2.ApplyFilterRequest
    join: _data_service_pb2.JoinRequest
    materialize: _data_service_pb2.MaterializeDataRequest
    parents: _containers.RepeatedCompositeFieldContainer[DataServiceRequestTree]
    def __init__(self, load_req: _Optional[_Union[_data_service_pb2.LoadDataRequest, _Mapping]] = ..., filter: _Optional[_Union[_data_service_pb2.ApplyFilterRequest, _Mapping]] = ..., join: _Optional[_Union[_data_service_pb2.JoinRequest, _Mapping]] = ..., materialize: _Optional[_Union[_data_service_pb2.MaterializeDataRequest, _Mapping]] = ..., parents: _Optional[_Iterable[_Union[DataServiceRequestTree, _Mapping]]] = ...) -> None: ...

class Schedule(_message.Message):
    __slots__ = ("schedule",)
    SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    schedule: _containers.RepeatedCompositeFieldContainer[CronElement]
    def __init__(self, schedule: _Optional[_Iterable[_Union[CronElement, _Mapping]]] = ...) -> None: ...

class CronElement(_message.Message):
    __slots__ = ("value", "repeat_every_value", "type")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    REPEAT_EVERY_VALUE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    value: _containers.RepeatedScalarFieldContainer[int]
    repeat_every_value: int
    type: CronElementType
    def __init__(self, value: _Optional[_Iterable[int]] = ..., repeat_every_value: _Optional[int] = ..., type: _Optional[_Union[CronElementType, str]] = ...) -> None: ...

class ScheduleIngestionResponse(_message.Message):
    __slots__ = ("workflow_id",)
    WORKFLOW_ID_FIELD_NUMBER: _ClassVar[int]
    workflow_id: str
    def __init__(self, workflow_id: _Optional[str] = ...) -> None: ...

class GetScheduleRequest(_message.Message):
    __slots__ = ("workflow_id",)
    WORKFLOW_ID_FIELD_NUMBER: _ClassVar[int]
    workflow_id: str
    def __init__(self, workflow_id: _Optional[str] = ...) -> None: ...

class GetScheduleResponse(_message.Message):
    __slots__ = ("request_template", "schedule", "run_results")
    REQUEST_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    RUN_RESULTS_FIELD_NUMBER: _ClassVar[int]
    request_template: DataServiceRequestTree
    schedule: Schedule
    run_results: _containers.RepeatedCompositeFieldContainer[RunResult]
    def __init__(self, request_template: _Optional[_Union[DataServiceRequestTree, _Mapping]] = ..., schedule: _Optional[_Union[Schedule, _Mapping]] = ..., run_results: _Optional[_Iterable[_Union[RunResult, _Mapping]]] = ...) -> None: ...

class RunResult(_message.Message):
    __slots__ = ("run_id", "started", "ended", "status", "materialize_operation_id", "error")
    class RunResultStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        RRS_INVALID: _ClassVar[RunResult.RunResultStatus]
        RRS_NOT_STARTED: _ClassVar[RunResult.RunResultStatus]
        RRS_STARTED: _ClassVar[RunResult.RunResultStatus]
        RRS_SUCCEDED: _ClassVar[RunResult.RunResultStatus]
        RRS_FAILED: _ClassVar[RunResult.RunResultStatus]
        RRS_CANCELED: _ClassVar[RunResult.RunResultStatus]
    RRS_INVALID: RunResult.RunResultStatus
    RRS_NOT_STARTED: RunResult.RunResultStatus
    RRS_STARTED: RunResult.RunResultStatus
    RRS_SUCCEDED: RunResult.RunResultStatus
    RRS_FAILED: RunResult.RunResultStatus
    RRS_CANCELED: RunResult.RunResultStatus
    RUN_ID_FIELD_NUMBER: _ClassVar[int]
    STARTED_FIELD_NUMBER: _ClassVar[int]
    ENDED_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MATERIALIZE_OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    run_id: str
    started: _timestamp_pb2.Timestamp
    ended: _timestamp_pb2.Timestamp
    status: RunResult.RunResultStatus
    materialize_operation_id: str
    error: str
    def __init__(self, run_id: _Optional[str] = ..., started: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., ended: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., status: _Optional[_Union[RunResult.RunResultStatus, str]] = ..., materialize_operation_id: _Optional[str] = ..., error: _Optional[str] = ...) -> None: ...

class GetWorkflowsRequest(_message.Message):
    __slots__ = ("project_id", "data_collection_id", "last_key", "limit")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_KEY_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    data_collection_id: str
    last_key: str
    limit: int
    def __init__(self, project_id: _Optional[str] = ..., data_collection_id: _Optional[str] = ..., last_key: _Optional[str] = ..., limit: _Optional[int] = ...) -> None: ...

class ScheduledIngestionInfo(_message.Message):
    __slots__ = ("workflow_id", "active")
    WORKFLOW_ID_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    workflow_id: str
    active: bool
    def __init__(self, workflow_id: _Optional[str] = ..., active: bool = ...) -> None: ...

class GetWorkflowsResponse(_message.Message):
    __slots__ = ("workflow_info", "has_more_data")
    WORKFLOW_INFO_FIELD_NUMBER: _ClassVar[int]
    HAS_MORE_DATA_FIELD_NUMBER: _ClassVar[int]
    workflow_info: _containers.RepeatedCompositeFieldContainer[ScheduledIngestionInfo]
    has_more_data: bool
    def __init__(self, workflow_info: _Optional[_Iterable[_Union[ScheduledIngestionInfo, _Mapping]]] = ..., has_more_data: bool = ...) -> None: ...

class CancelWorkflowRequest(_message.Message):
    __slots__ = ("workflow_id",)
    WORKFLOW_ID_FIELD_NUMBER: _ClassVar[int]
    workflow_id: str
    def __init__(self, workflow_id: _Optional[str] = ...) -> None: ...

class CancelWorkflowResponse(_message.Message):
    __slots__ = ("canceled_on",)
    CANCELED_ON_FIELD_NUMBER: _ClassVar[int]
    canceled_on: _timestamp_pb2.Timestamp
    def __init__(self, canceled_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class RunSingleIngestionRequest(_message.Message):
    __slots__ = ("request_template",)
    REQUEST_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    request_template: DataServiceRequestTree
    def __init__(self, request_template: _Optional[_Union[DataServiceRequestTree, _Mapping]] = ...) -> None: ...

class RunSingleIngestionResponse(_message.Message):
    __slots__ = ("workflow_id", "run_id")
    WORKFLOW_ID_FIELD_NUMBER: _ClassVar[int]
    RUN_ID_FIELD_NUMBER: _ClassVar[int]
    workflow_id: str
    run_id: str
    def __init__(self, workflow_id: _Optional[str] = ..., run_id: _Optional[str] = ...) -> None: ...

class RunSingleIngestionSyncRequest(_message.Message):
    __slots__ = ("request_template",)
    REQUEST_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    request_template: DataServiceRequestTree
    def __init__(self, request_template: _Optional[_Union[DataServiceRequestTree, _Mapping]] = ...) -> None: ...

class RunSingleIngestionSyncResponse(_message.Message):
    __slots__ = ("run_result",)
    RUN_RESULT_FIELD_NUMBER: _ClassVar[int]
    run_result: RunResult
    def __init__(self, run_result: _Optional[_Union[RunResult, _Mapping]] = ...) -> None: ...

class GetRunStatusRequest(_message.Message):
    __slots__ = ("workflow_id", "run_id")
    WORKFLOW_ID_FIELD_NUMBER: _ClassVar[int]
    RUN_ID_FIELD_NUMBER: _ClassVar[int]
    workflow_id: str
    run_id: str
    def __init__(self, workflow_id: _Optional[str] = ..., run_id: _Optional[str] = ...) -> None: ...

class GetRunStatusResponse(_message.Message):
    __slots__ = ("run_result",)
    RUN_RESULT_FIELD_NUMBER: _ClassVar[int]
    run_result: RunResult
    def __init__(self, run_result: _Optional[_Union[RunResult, _Mapping]] = ...) -> None: ...

class IngestDataRunResult(_message.Message):
    __slots__ = ("materialize_operation_id", "run_start", "time_range")
    MATERIALIZE_OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    RUN_START_FIELD_NUMBER: _ClassVar[int]
    TIME_RANGE_FIELD_NUMBER: _ClassVar[int]
    materialize_operation_id: str
    run_start: _timestamp_pb2.Timestamp
    time_range: _time_range_pb2.TimeRange
    def __init__(self, materialize_operation_id: _Optional[str] = ..., run_start: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., time_range: _Optional[_Union[_time_range_pb2.TimeRange, _Mapping]] = ...) -> None: ...
