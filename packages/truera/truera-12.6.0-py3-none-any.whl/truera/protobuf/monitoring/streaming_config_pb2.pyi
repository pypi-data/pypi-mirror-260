from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class StreamingWindowConfig(_message.Message):
    __slots__ = ("window_length_seconds", "window_slide_seconds", "trigger_length_seconds", "watermark_seconds")
    WINDOW_LENGTH_SECONDS_FIELD_NUMBER: _ClassVar[int]
    WINDOW_SLIDE_SECONDS_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_LENGTH_SECONDS_FIELD_NUMBER: _ClassVar[int]
    WATERMARK_SECONDS_FIELD_NUMBER: _ClassVar[int]
    window_length_seconds: int
    window_slide_seconds: int
    trigger_length_seconds: int
    watermark_seconds: int
    def __init__(self, window_length_seconds: _Optional[int] = ..., window_slide_seconds: _Optional[int] = ..., trigger_length_seconds: _Optional[int] = ..., watermark_seconds: _Optional[int] = ...) -> None: ...
