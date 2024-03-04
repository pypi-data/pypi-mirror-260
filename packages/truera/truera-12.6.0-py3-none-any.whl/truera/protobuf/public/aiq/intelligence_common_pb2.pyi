from truera.protobuf.public import truera_custom_options_pb2 as _truera_custom_options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ConfusionMatrixElements(_message.Message):
    __slots__ = ()
    class Element(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        INVALID: _ClassVar[ConfusionMatrixElements.Element]
        TRUE_POSITIVE: _ClassVar[ConfusionMatrixElements.Element]
        FALSE_POSITIVE: _ClassVar[ConfusionMatrixElements.Element]
        TRUE_NEGATIVE: _ClassVar[ConfusionMatrixElements.Element]
        FALSE_NEGATIVE: _ClassVar[ConfusionMatrixElements.Element]
    INVALID: ConfusionMatrixElements.Element
    TRUE_POSITIVE: ConfusionMatrixElements.Element
    FALSE_POSITIVE: ConfusionMatrixElements.Element
    TRUE_NEGATIVE: ConfusionMatrixElements.Element
    FALSE_NEGATIVE: ConfusionMatrixElements.Element
    def __init__(self) -> None: ...

class ProcessingMetadata(_message.Message):
    __slots__ = ("shuffled", "post_model_filter_thresh", "post_model_filter_labels")
    SHUFFLED_FIELD_NUMBER: _ClassVar[int]
    POST_MODEL_FILTER_THRESH_FIELD_NUMBER: _ClassVar[int]
    POST_MODEL_FILTER_LABELS_FIELD_NUMBER: _ClassVar[int]
    shuffled: bool
    post_model_filter_thresh: bool
    post_model_filter_labels: _containers.RepeatedScalarFieldContainer[ConfusionMatrixElements.Element]
    def __init__(self, shuffled: bool = ..., post_model_filter_thresh: bool = ..., post_model_filter_labels: _Optional[_Iterable[_Union[ConfusionMatrixElements.Element, str]]] = ...) -> None: ...
