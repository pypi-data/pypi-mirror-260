from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ScoreWrapper(_message.Message):
    __slots__ = ("proba_score", "classification_score", "regression_score", "logit_score", "tags")
    PROBA_SCORE_FIELD_NUMBER: _ClassVar[int]
    CLASSIFICATION_SCORE_FIELD_NUMBER: _ClassVar[int]
    REGRESSION_SCORE_FIELD_NUMBER: _ClassVar[int]
    LOGIT_SCORE_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    proba_score: float
    classification_score: str
    regression_score: float
    logit_score: float
    tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, proba_score: _Optional[float] = ..., classification_score: _Optional[str] = ..., regression_score: _Optional[float] = ..., logit_score: _Optional[float] = ..., tags: _Optional[_Iterable[str]] = ...) -> None: ...

class GroundTruth(_message.Message):
    __slots__ = ("regression_label", "classification_label")
    REGRESSION_LABEL_FIELD_NUMBER: _ClassVar[int]
    CLASSIFICATION_LABEL_FIELD_NUMBER: _ClassVar[int]
    regression_label: float
    classification_label: str
    def __init__(self, regression_label: _Optional[float] = ..., classification_label: _Optional[str] = ...) -> None: ...

class JoinedLabelPredictionData(_message.Message):
    __slots__ = ("timestamp", "prediction", "label", "model_id", "split_id", "tenant_id", "project_id", "data_collection_id")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    PREDICTION_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    prediction: _containers.RepeatedCompositeFieldContainer[ScoreWrapper]
    label: GroundTruth
    model_id: str
    split_id: str
    tenant_id: str
    project_id: str
    data_collection_id: str
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., prediction: _Optional[_Iterable[_Union[ScoreWrapper, _Mapping]]] = ..., label: _Optional[_Union[GroundTruth, _Mapping]] = ..., model_id: _Optional[str] = ..., split_id: _Optional[str] = ..., tenant_id: _Optional[str] = ..., project_id: _Optional[str] = ..., data_collection_id: _Optional[str] = ...) -> None: ...
