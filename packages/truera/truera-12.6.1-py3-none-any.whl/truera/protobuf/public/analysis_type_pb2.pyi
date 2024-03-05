from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class AnalysisType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN_ANALYSIS_TYPE: _ClassVar[AnalysisType]
    PREDICTIVE: _ClassVar[AnalysisType]
    GENERATIVE: _ClassVar[AnalysisType]
UNKNOWN_ANALYSIS_TYPE: AnalysisType
PREDICTIVE: AnalysisType
GENERATIVE: AnalysisType
