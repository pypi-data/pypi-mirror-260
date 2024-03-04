from google.api import annotations_pb2 as _annotations_pb2
from truera.protobuf.public.data import data_stream_ingestion_pb2 as _data_stream_ingestion_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SubscribeToTopicRequest(_message.Message):
    __slots__ = ("ingestion_id", "topic_name", "output_streams")
    INGESTION_ID_FIELD_NUMBER: _ClassVar[int]
    TOPIC_NAME_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_STREAMS_FIELD_NUMBER: _ClassVar[int]
    ingestion_id: str
    topic_name: str
    output_streams: _containers.RepeatedCompositeFieldContainer[_data_stream_ingestion_pb2.OutputStreamInfo]
    def __init__(self, ingestion_id: _Optional[str] = ..., topic_name: _Optional[str] = ..., output_streams: _Optional[_Iterable[_Union[_data_stream_ingestion_pb2.OutputStreamInfo, _Mapping]]] = ...) -> None: ...

class SubscribeToTopicResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class UnsubscribeFromTopicRequest(_message.Message):
    __slots__ = ("ingestion_id",)
    INGESTION_ID_FIELD_NUMBER: _ClassVar[int]
    ingestion_id: str
    def __init__(self, ingestion_id: _Optional[str] = ...) -> None: ...

class UnsubscribeFromTopicResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetStreamingRunnerStatusRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetStreamingRunnerStatusResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ShutdownStreamingRunnerRequest(_message.Message):
    __slots__ = ("shut_down_process",)
    SHUT_DOWN_PROCESS_FIELD_NUMBER: _ClassVar[int]
    shut_down_process: bool
    def __init__(self, shut_down_process: bool = ...) -> None: ...

class ShutdownStreamingRunnerResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
