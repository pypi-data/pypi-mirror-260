from truera.protobuf.public import common_pb2 as _common_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OptionsWithHash(_message.Message):
    __slots__ = ("options_hash", "prediction_options", "feature_influence_options")
    OPTIONS_HASH_FIELD_NUMBER: _ClassVar[int]
    PREDICTION_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    FEATURE_INFLUENCE_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    options_hash: str
    prediction_options: _common_pb2.PredictionOptions
    feature_influence_options: _common_pb2.FeatureInfluenceOptions
    def __init__(self, options_hash: _Optional[str] = ..., prediction_options: _Optional[_Union[_common_pb2.PredictionOptions, _Mapping]] = ..., feature_influence_options: _Optional[_Union[_common_pb2.FeatureInfluenceOptions, _Mapping]] = ...) -> None: ...
