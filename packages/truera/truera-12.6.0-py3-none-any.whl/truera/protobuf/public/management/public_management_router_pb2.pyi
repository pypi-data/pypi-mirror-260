from google.api import annotations_pb2 as _annotations_pb2
from truera.protobuf.public.management import management_service_pb2 as _management_service_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PublicManagementRouterPingRequest(_message.Message):
    __slots__ = ("test_string",)
    TEST_STRING_FIELD_NUMBER: _ClassVar[int]
    test_string: str
    def __init__(self, test_string: _Optional[str] = ...) -> None: ...

class PublicManagementRouterPingResponse(_message.Message):
    __slots__ = ("test_string",)
    TEST_STRING_FIELD_NUMBER: _ClassVar[int]
    test_string: str
    def __init__(self, test_string: _Optional[str] = ...) -> None: ...
