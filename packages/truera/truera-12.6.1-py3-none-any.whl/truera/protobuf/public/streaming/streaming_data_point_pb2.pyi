from google.protobuf import struct_pb2 as _struct_pb2
from truera.protobuf.public import qoi_pb2 as _qoi_pb2
from truera.protobuf.public import truera_custom_options_pb2 as _truera_custom_options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StreamingDataPoint(_message.Message):
    __slots__ = ("project_id", "data_collection_id", "split_id", "model_id", "score_type", "id", "timestamp", "data", "label", "extra", "prediction", "options_hash")
    class DataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...) -> None: ...
    class LabelEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...) -> None: ...
    class ExtraEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...) -> None: ...
    class PredictionEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...) -> None: ...
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    SCORE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    EXTRA_FIELD_NUMBER: _ClassVar[int]
    PREDICTION_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_HASH_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    data_collection_id: str
    split_id: str
    model_id: str
    score_type: _qoi_pb2.QuantityOfInterest
    id: str
    timestamp: str
    data: _containers.MessageMap[str, _struct_pb2.Value]
    label: _containers.MessageMap[str, _struct_pb2.Value]
    extra: _containers.MessageMap[str, _struct_pb2.Value]
    prediction: _containers.MessageMap[str, _struct_pb2.Value]
    options_hash: str
    def __init__(self, project_id: _Optional[str] = ..., data_collection_id: _Optional[str] = ..., split_id: _Optional[str] = ..., model_id: _Optional[str] = ..., score_type: _Optional[_Union[_qoi_pb2.QuantityOfInterest, str]] = ..., id: _Optional[str] = ..., timestamp: _Optional[str] = ..., data: _Optional[_Mapping[str, _struct_pb2.Value]] = ..., label: _Optional[_Mapping[str, _struct_pb2.Value]] = ..., extra: _Optional[_Mapping[str, _struct_pb2.Value]] = ..., prediction: _Optional[_Mapping[str, _struct_pb2.Value]] = ..., options_hash: _Optional[str] = ...) -> None: ...
