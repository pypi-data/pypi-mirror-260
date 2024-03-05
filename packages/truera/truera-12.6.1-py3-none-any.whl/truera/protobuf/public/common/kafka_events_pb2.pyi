from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SchemaMismatchKafkaRow(_message.Message):
    __slots__ = ("timestamp", "column_names")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    COLUMN_NAMES_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    column_names: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., column_names: _Optional[_Iterable[str]] = ...) -> None: ...

class OffsetTrackingEvent(_message.Message):
    __slots__ = ("batch_timestamp", "topic_name", "partition_offset_pairs")
    BATCH_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TOPIC_NAME_FIELD_NUMBER: _ClassVar[int]
    PARTITION_OFFSET_PAIRS_FIELD_NUMBER: _ClassVar[int]
    batch_timestamp: _timestamp_pb2.Timestamp
    topic_name: str
    partition_offset_pairs: _containers.RepeatedCompositeFieldContainer[PartitionOffsetPair]
    def __init__(self, batch_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., topic_name: _Optional[str] = ..., partition_offset_pairs: _Optional[_Iterable[_Union[PartitionOffsetPair, _Mapping]]] = ...) -> None: ...

class PartitionOffsetPair(_message.Message):
    __slots__ = ("partition", "offset")
    PARTITION_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    partition: int
    offset: int
    def __init__(self, partition: _Optional[int] = ..., offset: _Optional[int] = ...) -> None: ...
