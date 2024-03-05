from truera.protobuf.public.data import filter_pb2 as _filter_pb2
from truera.protobuf.public import truera_custom_options_pb2 as _truera_custom_options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Segmentation(_message.Message):
    __slots__ = ("id", "project_id", "segments", "has_other_segment", "name", "interesting_segment_info")
    ID_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SEGMENTS_FIELD_NUMBER: _ClassVar[int]
    HAS_OTHER_SEGMENT_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    INTERESTING_SEGMENT_INFO_FIELD_NUMBER: _ClassVar[int]
    id: str
    project_id: str
    segments: _containers.RepeatedCompositeFieldContainer[Segment]
    has_other_segment: bool
    name: str
    interesting_segment_info: InterestingSegmentInfo
    def __init__(self, id: _Optional[str] = ..., project_id: _Optional[str] = ..., segments: _Optional[_Iterable[_Union[Segment, _Mapping]]] = ..., has_other_segment: bool = ..., name: _Optional[str] = ..., interesting_segment_info: _Optional[_Union[InterestingSegmentInfo, _Mapping]] = ...) -> None: ...

class Segment(_message.Message):
    __slots__ = ("name", "filter_expression", "is_protected")
    NAME_FIELD_NUMBER: _ClassVar[int]
    FILTER_EXPRESSION_FIELD_NUMBER: _ClassVar[int]
    IS_PROTECTED_FIELD_NUMBER: _ClassVar[int]
    name: str
    filter_expression: _filter_pb2.FilterExpression
    is_protected: bool
    def __init__(self, name: _Optional[str] = ..., filter_expression: _Optional[_Union[_filter_pb2.FilterExpression, _Mapping]] = ..., is_protected: bool = ...) -> None: ...

class SegmentationCacheMetadata(_message.Message):
    __slots__ = ("id", "project_id", "segmentation_id", "split_id", "model_id", "location")
    ID_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SEGMENTATION_ID_FIELD_NUMBER: _ClassVar[int]
    SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    id: str
    project_id: str
    segmentation_id: str
    split_id: str
    model_id: str
    location: str
    def __init__(self, id: _Optional[str] = ..., project_id: _Optional[str] = ..., segmentation_id: _Optional[str] = ..., split_id: _Optional[str] = ..., model_id: _Optional[str] = ..., location: _Optional[str] = ...) -> None: ...

class InterestingSegmentInfo(_message.Message):
    __slots__ = ("model_id", "data_split_id", "hash", "type", "acceptance_state")
    class AcceptanceState(_message.Message):
        __slots__ = ()
        class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            UNKNOWN: _ClassVar[InterestingSegmentInfo.AcceptanceState.Type]
            ACCEPTED: _ClassVar[InterestingSegmentInfo.AcceptanceState.Type]
            REJECTED: _ClassVar[InterestingSegmentInfo.AcceptanceState.Type]
        UNKNOWN: InterestingSegmentInfo.AcceptanceState.Type
        ACCEPTED: InterestingSegmentInfo.AcceptanceState.Type
        REJECTED: InterestingSegmentInfo.AcceptanceState.Type
        def __init__(self) -> None: ...
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    HASH_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ACCEPTANCE_STATE_FIELD_NUMBER: _ClassVar[int]
    model_id: str
    data_split_id: str
    hash: str
    type: InterestingSegment.Type
    acceptance_state: InterestingSegmentInfo.AcceptanceState.Type
    def __init__(self, model_id: _Optional[str] = ..., data_split_id: _Optional[str] = ..., hash: _Optional[str] = ..., type: _Optional[_Union[InterestingSegment.Type, str]] = ..., acceptance_state: _Optional[_Union[InterestingSegmentInfo.AcceptanceState.Type, str]] = ...) -> None: ...

class InterestingSegment(_message.Message):
    __slots__ = ()
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[InterestingSegment.Type]
        HIGH_MEAN_ABSOLUTE_ERROR: _ClassVar[InterestingSegment.Type]
        LOW_POINTWISE_AUC: _ClassVar[InterestingSegment.Type]
        LOW_CLASSIFICATION_ACCURACY: _ClassVar[InterestingSegment.Type]
        OVERFITTING: _ClassVar[InterestingSegment.Type]
        HIGH_LOG_LOSS: _ClassVar[InterestingSegment.Type]
        HIGH_MEAN_SQUARED_ERROR: _ClassVar[InterestingSegment.Type]
        HIGH_MEAN_SQUARED_LOG_ERROR: _ClassVar[InterestingSegment.Type]
        LOW_PRECISION: _ClassVar[InterestingSegment.Type]
        LOW_RECALL: _ClassVar[InterestingSegment.Type]
        LOW_TRUE_POSITIVE_RATE: _ClassVar[InterestingSegment.Type]
        HIGH_FALSE_POSITIVE_RATE: _ClassVar[InterestingSegment.Type]
        LOW_TRUE_NEGATIVE_RATE: _ClassVar[InterestingSegment.Type]
        HIGH_FALSE_NEGATIVE_RATE: _ClassVar[InterestingSegment.Type]
        HIGH_UNDER_OR_OVERSAMPLING: _ClassVar[InterestingSegment.Type]
    UNKNOWN: InterestingSegment.Type
    HIGH_MEAN_ABSOLUTE_ERROR: InterestingSegment.Type
    LOW_POINTWISE_AUC: InterestingSegment.Type
    LOW_CLASSIFICATION_ACCURACY: InterestingSegment.Type
    OVERFITTING: InterestingSegment.Type
    HIGH_LOG_LOSS: InterestingSegment.Type
    HIGH_MEAN_SQUARED_ERROR: InterestingSegment.Type
    HIGH_MEAN_SQUARED_LOG_ERROR: InterestingSegment.Type
    LOW_PRECISION: InterestingSegment.Type
    LOW_RECALL: InterestingSegment.Type
    LOW_TRUE_POSITIVE_RATE: InterestingSegment.Type
    HIGH_FALSE_POSITIVE_RATE: InterestingSegment.Type
    LOW_TRUE_NEGATIVE_RATE: InterestingSegment.Type
    HIGH_FALSE_NEGATIVE_RATE: InterestingSegment.Type
    HIGH_UNDER_OR_OVERSAMPLING: InterestingSegment.Type
    def __init__(self) -> None: ...

class SegmentID(_message.Message):
    __slots__ = ("segmentation_id", "segment_name")
    SEGMENTATION_ID_FIELD_NUMBER: _ClassVar[int]
    SEGMENT_NAME_FIELD_NUMBER: _ClassVar[int]
    segmentation_id: str
    segment_name: str
    def __init__(self, segmentation_id: _Optional[str] = ..., segment_name: _Optional[str] = ...) -> None: ...
