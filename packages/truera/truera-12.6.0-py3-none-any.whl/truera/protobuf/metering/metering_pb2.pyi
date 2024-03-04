from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.api import annotations_pb2 as _annotations_pb2
from truera.protobuf.public.util import time_range_pb2 as _time_range_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ReportGranularity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN: _ClassVar[ReportGranularity]
    DAY: _ClassVar[ReportGranularity]
    CUMULATIVE: _ClassVar[ReportGranularity]
UNKNOWN: ReportGranularity
DAY: ReportGranularity
CUMULATIVE: ReportGranularity

class MeteringPingRequest(_message.Message):
    __slots__ = ("ping_string",)
    PING_STRING_FIELD_NUMBER: _ClassVar[int]
    ping_string: str
    def __init__(self, ping_string: _Optional[str] = ...) -> None: ...

class MeteringPingResponse(_message.Message):
    __slots__ = ("ping_response",)
    PING_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    ping_response: str
    def __init__(self, ping_response: _Optional[str] = ...) -> None: ...

class MonthlyMeteringWindow(_message.Message):
    __slots__ = ("year", "month", "time_zone")
    YEAR_FIELD_NUMBER: _ClassVar[int]
    MONTH_FIELD_NUMBER: _ClassVar[int]
    TIME_ZONE_FIELD_NUMBER: _ClassVar[int]
    year: int
    month: int
    time_zone: str
    def __init__(self, year: _Optional[int] = ..., month: _Optional[int] = ..., time_zone: _Optional[str] = ...) -> None: ...

class MeteringWindow(_message.Message):
    __slots__ = ("monthly_metering_window", "timestamp_metering_window")
    MONTHLY_METERING_WINDOW_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_METERING_WINDOW_FIELD_NUMBER: _ClassVar[int]
    monthly_metering_window: MonthlyMeteringWindow
    timestamp_metering_window: _time_range_pb2.TimeRange
    def __init__(self, monthly_metering_window: _Optional[_Union[MonthlyMeteringWindow, _Mapping]] = ..., timestamp_metering_window: _Optional[_Union[_time_range_pb2.TimeRange, _Mapping]] = ...) -> None: ...

class MeteringIngestionStatsRequest(_message.Message):
    __slots__ = ("tenant_id", "metering_window", "report_granularity", "workspace_id")
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    METERING_WINDOW_FIELD_NUMBER: _ClassVar[int]
    REPORT_GRANULARITY_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    tenant_id: str
    metering_window: MeteringWindow
    report_granularity: ReportGranularity
    workspace_id: str
    def __init__(self, tenant_id: _Optional[str] = ..., metering_window: _Optional[_Union[MeteringWindow, _Mapping]] = ..., report_granularity: _Optional[_Union[ReportGranularity, str]] = ..., workspace_id: _Optional[str] = ...) -> None: ...

class MeteringIngestionStatsResponse(_message.Message):
    __slots__ = ("tenant_id", "metering_window", "last_updated_timestamp", "metering_ingestion_stats_entry")
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    METERING_WINDOW_FIELD_NUMBER: _ClassVar[int]
    LAST_UPDATED_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    METERING_INGESTION_STATS_ENTRY_FIELD_NUMBER: _ClassVar[int]
    tenant_id: str
    metering_window: MeteringWindow
    last_updated_timestamp: _timestamp_pb2.Timestamp
    metering_ingestion_stats_entry: _containers.RepeatedCompositeFieldContainer[MeteringIngestionStatsEntry]
    def __init__(self, tenant_id: _Optional[str] = ..., metering_window: _Optional[_Union[MeteringWindow, _Mapping]] = ..., last_updated_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., metering_ingestion_stats_entry: _Optional[_Iterable[_Union[MeteringIngestionStatsEntry, _Mapping]]] = ...) -> None: ...

class MeteringIngestionStatsEntry(_message.Message):
    __slots__ = ("time_range", "project_id", "data_collection_id", "column_count", "rows_ingested")
    TIME_RANGE_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    COLUMN_COUNT_FIELD_NUMBER: _ClassVar[int]
    ROWS_INGESTED_FIELD_NUMBER: _ClassVar[int]
    time_range: _time_range_pb2.TimeRange
    project_id: str
    data_collection_id: str
    column_count: int
    rows_ingested: int
    def __init__(self, time_range: _Optional[_Union[_time_range_pb2.TimeRange, _Mapping]] = ..., project_id: _Optional[str] = ..., data_collection_id: _Optional[str] = ..., column_count: _Optional[int] = ..., rows_ingested: _Optional[int] = ...) -> None: ...
