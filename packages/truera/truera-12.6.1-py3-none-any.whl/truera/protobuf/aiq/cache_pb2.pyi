from truera.protobuf.aiq import config_pb2 as _config_pb2
from truera.protobuf.public import qoi_pb2 as _qoi_pb2
from truera.protobuf.public.aiq import intelligence_common_pb2 as _intelligence_common_pb2
from truera.protobuf.public.aiq import intelligence_service_pb2 as _intelligence_service_pb2
from truera.protobuf.public import background_data_split_info_pb2 as _background_data_split_info_pb2
from truera.protobuf.public import truera_custom_options_pb2 as _truera_custom_options_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ExplanationCacheMetadata(_message.Message):
    __slots__ = ("id", "model_id", "model_input_spec", "intervention_data_split_id", "background_data_split_info", "score_type", "config", "location", "format", "generated_by", "processing", "explanation_cache_type", "updated_on")
    class ExplanationCacheType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        FEATURE_INFLUENCE: _ClassVar[ExplanationCacheMetadata.ExplanationCacheType]
        PARTIAL_DEPENDENCE: _ClassVar[ExplanationCacheMetadata.ExplanationCacheType]
        FEATURE_INFLUENCE_KERNEL_SHAP: _ClassVar[ExplanationCacheMetadata.ExplanationCacheType]
        FEATURE_INFLUENCE_TREE_SHAP_INTERVENTIONAL: _ClassVar[ExplanationCacheMetadata.ExplanationCacheType]
        FEATURE_INFLUENCE_TREE_SHAP_PATH_DEPENDENT: _ClassVar[ExplanationCacheMetadata.ExplanationCacheType]
        FEATURE_INFLUENCE_INTEGRATED_GRADIENTS: _ClassVar[ExplanationCacheMetadata.ExplanationCacheType]
        FEATURE_INFLUENCE_NLP_SHAP: _ClassVar[ExplanationCacheMetadata.ExplanationCacheType]
    FEATURE_INFLUENCE: ExplanationCacheMetadata.ExplanationCacheType
    PARTIAL_DEPENDENCE: ExplanationCacheMetadata.ExplanationCacheType
    FEATURE_INFLUENCE_KERNEL_SHAP: ExplanationCacheMetadata.ExplanationCacheType
    FEATURE_INFLUENCE_TREE_SHAP_INTERVENTIONAL: ExplanationCacheMetadata.ExplanationCacheType
    FEATURE_INFLUENCE_TREE_SHAP_PATH_DEPENDENT: ExplanationCacheMetadata.ExplanationCacheType
    FEATURE_INFLUENCE_INTEGRATED_GRADIENTS: ExplanationCacheMetadata.ExplanationCacheType
    FEATURE_INFLUENCE_NLP_SHAP: ExplanationCacheMetadata.ExplanationCacheType
    ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_INPUT_SPEC_FIELD_NUMBER: _ClassVar[int]
    INTERVENTION_DATA_SPLIT_ID_FIELD_NUMBER: _ClassVar[int]
    BACKGROUND_DATA_SPLIT_INFO_FIELD_NUMBER: _ClassVar[int]
    SCORE_TYPE_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    GENERATED_BY_FIELD_NUMBER: _ClassVar[int]
    PROCESSING_FIELD_NUMBER: _ClassVar[int]
    EXPLANATION_CACHE_TYPE_FIELD_NUMBER: _ClassVar[int]
    UPDATED_ON_FIELD_NUMBER: _ClassVar[int]
    id: str
    model_id: _intelligence_service_pb2.ModelId
    model_input_spec: _intelligence_service_pb2.ModelInputSpec
    intervention_data_split_id: str
    background_data_split_info: _background_data_split_info_pb2.BackgroundDataSplitInfo
    score_type: _qoi_pb2.QuantityOfInterest
    config: _config_pb2.AnalyticsConfig
    location: str
    format: str
    generated_by: str
    processing: _intelligence_common_pb2.ProcessingMetadata
    explanation_cache_type: ExplanationCacheMetadata.ExplanationCacheType
    updated_on: str
    def __init__(self, id: _Optional[str] = ..., model_id: _Optional[_Union[_intelligence_service_pb2.ModelId, _Mapping]] = ..., model_input_spec: _Optional[_Union[_intelligence_service_pb2.ModelInputSpec, _Mapping]] = ..., intervention_data_split_id: _Optional[str] = ..., background_data_split_info: _Optional[_Union[_background_data_split_info_pb2.BackgroundDataSplitInfo, _Mapping]] = ..., score_type: _Optional[_Union[_qoi_pb2.QuantityOfInterest, str]] = ..., config: _Optional[_Union[_config_pb2.AnalyticsConfig, _Mapping]] = ..., location: _Optional[str] = ..., format: _Optional[str] = ..., generated_by: _Optional[str] = ..., processing: _Optional[_Union[_intelligence_common_pb2.ProcessingMetadata, _Mapping]] = ..., explanation_cache_type: _Optional[_Union[ExplanationCacheMetadata.ExplanationCacheType, str]] = ..., updated_on: _Optional[str] = ...) -> None: ...

class ModelPredictionCacheMetadata(_message.Message):
    __slots__ = ("id", "model_id", "model_input_spec", "score_type", "location", "format", "generated_by", "processing")
    ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_INPUT_SPEC_FIELD_NUMBER: _ClassVar[int]
    SCORE_TYPE_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    GENERATED_BY_FIELD_NUMBER: _ClassVar[int]
    PROCESSING_FIELD_NUMBER: _ClassVar[int]
    id: str
    model_id: _intelligence_service_pb2.ModelId
    model_input_spec: _intelligence_service_pb2.ModelInputSpec
    score_type: _qoi_pb2.QuantityOfInterest
    location: str
    format: str
    generated_by: str
    processing: _intelligence_common_pb2.ProcessingMetadata
    def __init__(self, id: _Optional[str] = ..., model_id: _Optional[_Union[_intelligence_service_pb2.ModelId, _Mapping]] = ..., model_input_spec: _Optional[_Union[_intelligence_service_pb2.ModelInputSpec, _Mapping]] = ..., score_type: _Optional[_Union[_qoi_pb2.QuantityOfInterest, str]] = ..., location: _Optional[str] = ..., format: _Optional[str] = ..., generated_by: _Optional[str] = ..., processing: _Optional[_Union[_intelligence_common_pb2.ProcessingMetadata, _Mapping]] = ...) -> None: ...
