from truera.protobuf.public import truera_custom_options_pb2 as _truera_custom_options_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MonitoringConfig(_message.Message):
    __slots__ = ("id", "project_id", "model_id", "dashboard_range", "enabled")
    class DashboardRange(_message.Message):
        __slots__ = ("begin_time", "end_time")
        BEGIN_TIME_FIELD_NUMBER: _ClassVar[int]
        END_TIME_FIELD_NUMBER: _ClassVar[int]
        begin_time: str
        end_time: str
        def __init__(self, begin_time: _Optional[str] = ..., end_time: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    DASHBOARD_RANGE_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    id: str
    project_id: str
    model_id: str
    dashboard_range: MonitoringConfig.DashboardRange
    enabled: bool
    def __init__(self, id: _Optional[str] = ..., project_id: _Optional[str] = ..., model_id: _Optional[str] = ..., dashboard_range: _Optional[_Union[MonitoringConfig.DashboardRange, _Mapping]] = ..., enabled: bool = ...) -> None: ...
