from truera.protobuf.public import truera_custom_options_pb2 as _truera_custom_options_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class QuantityOfInterest(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN_QOI: _ClassVar[QuantityOfInterest]
    LOGITS_SCORE: _ClassVar[QuantityOfInterest]
    PROBITS_SCORE: _ClassVar[QuantityOfInterest]
    CLASSIFICATION_SCORE: _ClassVar[QuantityOfInterest]
    REGRESSION_SCORE: _ClassVar[QuantityOfInterest]
    LOG_LOSS: _ClassVar[QuantityOfInterest]
    MEAN_ABSOLUTE_ERROR_FOR_CLASSIFICATION: _ClassVar[QuantityOfInterest]
    MEAN_ABSOLUTE_ERROR_FOR_REGRESSION: _ClassVar[QuantityOfInterest]
    RANK: _ClassVar[QuantityOfInterest]
    RANKING_SCORE: _ClassVar[QuantityOfInterest]
    GENERATIVE_TEXT: _ClassVar[QuantityOfInterest]

class ExplanationAlgorithmType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EXPLANATION_ALGORITHM_UNKNOWN: _ClassVar[ExplanationAlgorithmType]
    TRUERA_QII: _ClassVar[ExplanationAlgorithmType]
    KERNEL_SHAP: _ClassVar[ExplanationAlgorithmType]
    TREE_SHAP_INTERVENTIONAL: _ClassVar[ExplanationAlgorithmType]
    TREE_SHAP_PATH_DEPENDENT: _ClassVar[ExplanationAlgorithmType]
    INTEGRATED_GRADIENTS: _ClassVar[ExplanationAlgorithmType]
    NLP_SHAP: _ClassVar[ExplanationAlgorithmType]
UNKNOWN_QOI: QuantityOfInterest
LOGITS_SCORE: QuantityOfInterest
PROBITS_SCORE: QuantityOfInterest
CLASSIFICATION_SCORE: QuantityOfInterest
REGRESSION_SCORE: QuantityOfInterest
LOG_LOSS: QuantityOfInterest
MEAN_ABSOLUTE_ERROR_FOR_CLASSIFICATION: QuantityOfInterest
MEAN_ABSOLUTE_ERROR_FOR_REGRESSION: QuantityOfInterest
RANK: QuantityOfInterest
RANKING_SCORE: QuantityOfInterest
GENERATIVE_TEXT: QuantityOfInterest
EXPLANATION_ALGORITHM_UNKNOWN: ExplanationAlgorithmType
TRUERA_QII: ExplanationAlgorithmType
KERNEL_SHAP: ExplanationAlgorithmType
TREE_SHAP_INTERVENTIONAL: ExplanationAlgorithmType
TREE_SHAP_PATH_DEPENDENT: ExplanationAlgorithmType
INTEGRATED_GRADIENTS: ExplanationAlgorithmType
NLP_SHAP: ExplanationAlgorithmType
