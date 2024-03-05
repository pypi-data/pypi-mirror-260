from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from truera.protobuf.public.util import time_range_pb2 as _time_range_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BillingMetrics(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNDEFINED: _ClassVar[BillingMetrics]
    PROJECT: _ClassVar[BillingMetrics]
    USER: _ClassVar[BillingMetrics]

class AuditSummaryMetrics(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    USERS_ACTIVE: _ClassVar[AuditSummaryMetrics]
    USERS_TAKING_ADMIN_ACTIONS: _ClassVar[AuditSummaryMetrics]
UNDEFINED: BillingMetrics
PROJECT: BillingMetrics
USER: BillingMetrics
USERS_ACTIVE: AuditSummaryMetrics
USERS_TAKING_ADMIN_ACTIONS: AuditSummaryMetrics

class ListBillingMetricsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListBillingMetricsResponse(_message.Message):
    __slots__ = ("metrics",)
    METRICS_FIELD_NUMBER: _ClassVar[int]
    metrics: _containers.RepeatedScalarFieldContainer[BillingMetrics]
    def __init__(self, metrics: _Optional[_Iterable[_Union[BillingMetrics, str]]] = ...) -> None: ...

class GenerateUsageReportRequest(_message.Message):
    __slots__ = ("reportDateRange",)
    REPORTDATERANGE_FIELD_NUMBER: _ClassVar[int]
    reportDateRange: _time_range_pb2.TimeRange
    def __init__(self, reportDateRange: _Optional[_Union[_time_range_pb2.TimeRange, _Mapping]] = ...) -> None: ...

class GenerateUsageReportResponse(_message.Message):
    __slots__ = ("reportDateRange", "generatedAt", "metricsDetails")
    REPORTDATERANGE_FIELD_NUMBER: _ClassVar[int]
    GENERATEDAT_FIELD_NUMBER: _ClassVar[int]
    METRICSDETAILS_FIELD_NUMBER: _ClassVar[int]
    reportDateRange: _time_range_pb2.TimeRange
    generatedAt: _timestamp_pb2.Timestamp
    metricsDetails: _containers.RepeatedCompositeFieldContainer[MetricsDetails]
    def __init__(self, reportDateRange: _Optional[_Union[_time_range_pb2.TimeRange, _Mapping]] = ..., generatedAt: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., metricsDetails: _Optional[_Iterable[_Union[MetricsDetails, _Mapping]]] = ...) -> None: ...

class MetricsDetails(_message.Message):
    __slots__ = ("name", "summary", "details")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    name: str
    summary: Summary
    details: Detail
    def __init__(self, name: _Optional[str] = ..., summary: _Optional[_Union[Summary, _Mapping]] = ..., details: _Optional[_Union[Detail, _Mapping]] = ...) -> None: ...

class Summary(_message.Message):
    __slots__ = ("New", "Deleted", "StartCount", "EndCount")
    NEW_FIELD_NUMBER: _ClassVar[int]
    DELETED_FIELD_NUMBER: _ClassVar[int]
    STARTCOUNT_FIELD_NUMBER: _ClassVar[int]
    ENDCOUNT_FIELD_NUMBER: _ClassVar[int]
    New: int
    Deleted: int
    StartCount: int
    EndCount: int
    def __init__(self, New: _Optional[int] = ..., Deleted: _Optional[int] = ..., StartCount: _Optional[int] = ..., EndCount: _Optional[int] = ...) -> None: ...

class Detail(_message.Message):
    __slots__ = ("entryDetails",)
    ENTRYDETAILS_FIELD_NUMBER: _ClassVar[int]
    entryDetails: _containers.RepeatedCompositeFieldContainer[EntryDetail]
    def __init__(self, entryDetails: _Optional[_Iterable[_Union[EntryDetail, _Mapping]]] = ...) -> None: ...

class EntryDetail(_message.Message):
    __slots__ = ("EntryName", "CreatedAt")
    ENTRYNAME_FIELD_NUMBER: _ClassVar[int]
    CREATEDAT_FIELD_NUMBER: _ClassVar[int]
    EntryName: str
    CreatedAt: str
    def __init__(self, EntryName: _Optional[str] = ..., CreatedAt: _Optional[str] = ...) -> None: ...

class ListAuditSummaryMetricsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListAuditSummaryMetricsResponse(_message.Message):
    __slots__ = ("metrics",)
    METRICS_FIELD_NUMBER: _ClassVar[int]
    metrics: _containers.RepeatedScalarFieldContainer[AuditSummaryMetrics]
    def __init__(self, metrics: _Optional[_Iterable[_Union[AuditSummaryMetrics, str]]] = ...) -> None: ...

class GenerateAuditSummaryReportRequest(_message.Message):
    __slots__ = ("reportDateRange", "metrics")
    REPORTDATERANGE_FIELD_NUMBER: _ClassVar[int]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    reportDateRange: _time_range_pb2.TimeRange
    metrics: _containers.RepeatedScalarFieldContainer[AuditSummaryMetrics]
    def __init__(self, reportDateRange: _Optional[_Union[_time_range_pb2.TimeRange, _Mapping]] = ..., metrics: _Optional[_Iterable[_Union[AuditSummaryMetrics, str]]] = ...) -> None: ...

class GenerateAuditSummaryReportResponse(_message.Message):
    __slots__ = ("reportDateRange", "generatedAt", "metricsDetails")
    REPORTDATERANGE_FIELD_NUMBER: _ClassVar[int]
    GENERATEDAT_FIELD_NUMBER: _ClassVar[int]
    METRICSDETAILS_FIELD_NUMBER: _ClassVar[int]
    reportDateRange: _time_range_pb2.TimeRange
    generatedAt: _timestamp_pb2.Timestamp
    metricsDetails: _containers.RepeatedCompositeFieldContainer[AuditMetricsDetails]
    def __init__(self, reportDateRange: _Optional[_Union[_time_range_pb2.TimeRange, _Mapping]] = ..., generatedAt: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., metricsDetails: _Optional[_Iterable[_Union[AuditMetricsDetails, _Mapping]]] = ...) -> None: ...

class AuditMetricsDetails(_message.Message):
    __slots__ = ("name", "auditSummary", "auditDetails")
    NAME_FIELD_NUMBER: _ClassVar[int]
    AUDITSUMMARY_FIELD_NUMBER: _ClassVar[int]
    AUDITDETAILS_FIELD_NUMBER: _ClassVar[int]
    name: str
    auditSummary: AuditSummary
    auditDetails: AuditDetails
    def __init__(self, name: _Optional[str] = ..., auditSummary: _Optional[_Union[AuditSummary, _Mapping]] = ..., auditDetails: _Optional[_Union[AuditDetails, _Mapping]] = ...) -> None: ...

class AuditSummary(_message.Message):
    __slots__ = ("count",)
    COUNT_FIELD_NUMBER: _ClassVar[int]
    count: int
    def __init__(self, count: _Optional[int] = ...) -> None: ...

class AuditDetails(_message.Message):
    __slots__ = ("auditEntryDetails",)
    AUDITENTRYDETAILS_FIELD_NUMBER: _ClassVar[int]
    auditEntryDetails: _containers.RepeatedCompositeFieldContainer[AuditEntryDetail]
    def __init__(self, auditEntryDetails: _Optional[_Iterable[_Union[AuditEntryDetail, _Mapping]]] = ...) -> None: ...

class AuditEntryDetail(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...
