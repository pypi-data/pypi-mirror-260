from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import wrappers_pb2 as _wrappers_pb2
from truera.protobuf.public import truera_custom_options_pb2 as _truera_custom_options_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GenerativeCost(_message.Message):
    __slots__ = ("n_requests", "n_successful_requests", "n_classes", "n_tokens", "n_stream_chunks", "n_prompt_tokens", "n_completion_tokens", "cost")
    N_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    N_SUCCESSFUL_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    N_CLASSES_FIELD_NUMBER: _ClassVar[int]
    N_TOKENS_FIELD_NUMBER: _ClassVar[int]
    N_STREAM_CHUNKS_FIELD_NUMBER: _ClassVar[int]
    N_PROMPT_TOKENS_FIELD_NUMBER: _ClassVar[int]
    N_COMPLETION_TOKENS_FIELD_NUMBER: _ClassVar[int]
    COST_FIELD_NUMBER: _ClassVar[int]
    n_requests: _wrappers_pb2.Int32Value
    n_successful_requests: _wrappers_pb2.Int32Value
    n_classes: _wrappers_pb2.Int32Value
    n_tokens: _wrappers_pb2.Int32Value
    n_stream_chunks: _wrappers_pb2.Int32Value
    n_prompt_tokens: _wrappers_pb2.Int32Value
    n_completion_tokens: _wrappers_pb2.Int32Value
    cost: _wrappers_pb2.DoubleValue
    def __init__(self, n_requests: _Optional[_Union[_wrappers_pb2.Int32Value, _Mapping]] = ..., n_successful_requests: _Optional[_Union[_wrappers_pb2.Int32Value, _Mapping]] = ..., n_classes: _Optional[_Union[_wrappers_pb2.Int32Value, _Mapping]] = ..., n_tokens: _Optional[_Union[_wrappers_pb2.Int32Value, _Mapping]] = ..., n_stream_chunks: _Optional[_Union[_wrappers_pb2.Int32Value, _Mapping]] = ..., n_prompt_tokens: _Optional[_Union[_wrappers_pb2.Int32Value, _Mapping]] = ..., n_completion_tokens: _Optional[_Union[_wrappers_pb2.Int32Value, _Mapping]] = ..., cost: _Optional[_Union[_wrappers_pb2.DoubleValue, _Mapping]] = ...) -> None: ...

class GenerativeFeedback(_message.Message):
    __slots__ = ("feedback_function_id", "feedback_result_id", "record_id", "result", "meta", "cost", "evaluation_timestamp", "calls")
    FEEDBACK_FUNCTION_ID_FIELD_NUMBER: _ClassVar[int]
    FEEDBACK_RESULT_ID_FIELD_NUMBER: _ClassVar[int]
    RECORD_ID_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    META_FIELD_NUMBER: _ClassVar[int]
    COST_FIELD_NUMBER: _ClassVar[int]
    EVALUATION_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    CALLS_FIELD_NUMBER: _ClassVar[int]
    feedback_function_id: str
    feedback_result_id: str
    record_id: str
    result: float
    meta: _struct_pb2.Value
    cost: GenerativeCost
    evaluation_timestamp: _timestamp_pb2.Timestamp
    calls: _struct_pb2.Value
    def __init__(self, feedback_function_id: _Optional[str] = ..., feedback_result_id: _Optional[str] = ..., record_id: _Optional[str] = ..., result: _Optional[float] = ..., meta: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ..., cost: _Optional[_Union[GenerativeCost, _Mapping]] = ..., evaluation_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., calls: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...) -> None: ...

class GenerativeTrace(_message.Message):
    __slots__ = ("record_id", "cost", "meta", "main_input", "main_output", "main_error", "calls", "prompt", "start_time", "end_time")
    RECORD_ID_FIELD_NUMBER: _ClassVar[int]
    COST_FIELD_NUMBER: _ClassVar[int]
    META_FIELD_NUMBER: _ClassVar[int]
    MAIN_INPUT_FIELD_NUMBER: _ClassVar[int]
    MAIN_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    MAIN_ERROR_FIELD_NUMBER: _ClassVar[int]
    CALLS_FIELD_NUMBER: _ClassVar[int]
    PROMPT_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    record_id: str
    cost: GenerativeCost
    meta: _struct_pb2.Value
    main_input: _struct_pb2.Value
    main_output: _struct_pb2.Value
    main_error: _struct_pb2.Value
    calls: _struct_pb2.Value
    prompt: _struct_pb2.Value
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    def __init__(self, record_id: _Optional[str] = ..., cost: _Optional[_Union[GenerativeCost, _Mapping]] = ..., meta: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ..., main_input: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ..., main_output: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ..., main_error: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ..., calls: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ..., prompt: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ..., start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
