from google.api import annotations_pb2 as _annotations_pb2
from truera.protobuf.public import truera_custom_options_pb2 as _truera_custom_options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PingRequest(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class PingResponse(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class GetBatchesForSinkRequest(_message.Message):
    __slots__ = ("data_collection_id", "sink_name")
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    SINK_NAME_FIELD_NUMBER: _ClassVar[int]
    data_collection_id: str
    sink_name: str
    def __init__(self, data_collection_id: _Optional[str] = ..., sink_name: _Optional[str] = ...) -> None: ...

class GetBatchesForSinkResponse(_message.Message):
    __slots__ = ("batch_ids",)
    BATCH_IDS_FIELD_NUMBER: _ClassVar[int]
    batch_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, batch_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class GetPointsForBatchRequest(_message.Message):
    __slots__ = ("data_collection_id", "batch_id", "sink_name")
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    BATCH_ID_FIELD_NUMBER: _ClassVar[int]
    SINK_NAME_FIELD_NUMBER: _ClassVar[int]
    data_collection_id: str
    batch_id: str
    sink_name: str
    def __init__(self, data_collection_id: _Optional[str] = ..., batch_id: _Optional[str] = ..., sink_name: _Optional[str] = ...) -> None: ...

class GetPointsForBatchResponse(_message.Message):
    __slots__ = ("total_count",)
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    total_count: int
    def __init__(self, total_count: _Optional[int] = ...) -> None: ...

class GetRecentWindowsRequest(_message.Message):
    __slots__ = ("data_collection_id", "batch_id", "sink_name")
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    BATCH_ID_FIELD_NUMBER: _ClassVar[int]
    SINK_NAME_FIELD_NUMBER: _ClassVar[int]
    data_collection_id: str
    batch_id: str
    sink_name: str
    def __init__(self, data_collection_id: _Optional[str] = ..., batch_id: _Optional[str] = ..., sink_name: _Optional[str] = ...) -> None: ...

class ObservationWindow(_message.Message):
    __slots__ = ("num_points", "start_time", "end_time")
    NUM_POINTS_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    num_points: int
    start_time: int
    end_time: int
    def __init__(self, num_points: _Optional[int] = ..., start_time: _Optional[int] = ..., end_time: _Optional[int] = ...) -> None: ...

class GetRecentWindowsResponse(_message.Message):
    __slots__ = ("num_windows", "windows")
    NUM_WINDOWS_FIELD_NUMBER: _ClassVar[int]
    WINDOWS_FIELD_NUMBER: _ClassVar[int]
    num_windows: int
    windows: _containers.RepeatedCompositeFieldContainer[ObservationWindow]
    def __init__(self, num_windows: _Optional[int] = ..., windows: _Optional[_Iterable[_Union[ObservationWindow, _Mapping]]] = ...) -> None: ...
