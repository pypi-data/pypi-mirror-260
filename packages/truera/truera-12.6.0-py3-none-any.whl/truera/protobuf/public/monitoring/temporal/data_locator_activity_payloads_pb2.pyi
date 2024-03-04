from truera.protobuf.public.common import data_locator_pb2 as _data_locator_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SearchDataLocatorsResponse(_message.Message):
    __slots__ = ("data_locators",)
    DATA_LOCATORS_FIELD_NUMBER: _ClassVar[int]
    data_locators: _containers.RepeatedCompositeFieldContainer[_data_locator_pb2.DataLocator]
    def __init__(self, data_locators: _Optional[_Iterable[_Union[_data_locator_pb2.DataLocator, _Mapping]]] = ...) -> None: ...
