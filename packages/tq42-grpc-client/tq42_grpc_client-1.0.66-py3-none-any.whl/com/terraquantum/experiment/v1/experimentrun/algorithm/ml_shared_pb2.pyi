from com.terraquantum.experiment.v1.experimentrun.algorithm import shared_pb2 as _shared_pb2
from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OptimProto(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OPTIM_UNSPECIFIED: _ClassVar[OptimProto]
    ADAM: _ClassVar[OptimProto]
    ADAMW: _ClassVar[OptimProto]
    SGD: _ClassVar[OptimProto]

class LossFuncProto(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LOSS_FUNC_UNSPECIFIED: _ClassVar[LossFuncProto]
    MSE: _ClassVar[LossFuncProto]
    MAE: _ClassVar[LossFuncProto]
    BCE: _ClassVar[LossFuncProto]
    CROSSENTROPY: _ClassVar[LossFuncProto]
OPTIM_UNSPECIFIED: OptimProto
ADAM: OptimProto
ADAMW: OptimProto
SGD: OptimProto
LOSS_FUNC_UNSPECIFIED: LossFuncProto
MSE: LossFuncProto
MAE: LossFuncProto
BCE: LossFuncProto
CROSSENTROPY: LossFuncProto

class MLTrainInputsProto(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _shared_pb2.DatasetStorageInfoProto
    def __init__(self, data: _Optional[_Union[_shared_pb2.DatasetStorageInfoProto, _Mapping]] = ...) -> None: ...

class MLTrainOutputsProto(_message.Message):
    __slots__ = ("model",)
    MODEL_FIELD_NUMBER: _ClassVar[int]
    model: _shared_pb2.ModelStorageInfoProto
    def __init__(self, model: _Optional[_Union[_shared_pb2.ModelStorageInfoProto, _Mapping]] = ...) -> None: ...

class Metrics(_message.Message):
    __slots__ = ("mse", "mae")
    MSE_FIELD_NUMBER: _ClassVar[int]
    MAE_FIELD_NUMBER: _ClassVar[int]
    mse: float
    mae: float
    def __init__(self, mse: _Optional[float] = ..., mae: _Optional[float] = ...) -> None: ...

class TSTrainResultProto(_message.Message):
    __slots__ = ("train_losses", "test_losses", "version", "original_outputs", "train_metrics", "test_metrics", "timestamp", "evaluation_outputs", "time_label", "output_label", "output_scale")
    TRAIN_LOSSES_FIELD_NUMBER: _ClassVar[int]
    TEST_LOSSES_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    TRAIN_METRICS_FIELD_NUMBER: _ClassVar[int]
    TEST_METRICS_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    EVALUATION_OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    TIME_LABEL_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_LABEL_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_SCALE_FIELD_NUMBER: _ClassVar[int]
    train_losses: _containers.RepeatedScalarFieldContainer[float]
    test_losses: _containers.RepeatedScalarFieldContainer[float]
    version: str
    original_outputs: _containers.RepeatedScalarFieldContainer[float]
    train_metrics: Metrics
    test_metrics: Metrics
    timestamp: _containers.RepeatedScalarFieldContainer[str]
    evaluation_outputs: _containers.RepeatedScalarFieldContainer[float]
    time_label: str
    output_label: str
    output_scale: float
    def __init__(self, train_losses: _Optional[_Iterable[float]] = ..., test_losses: _Optional[_Iterable[float]] = ..., version: _Optional[str] = ..., original_outputs: _Optional[_Iterable[float]] = ..., train_metrics: _Optional[_Union[Metrics, _Mapping]] = ..., test_metrics: _Optional[_Union[Metrics, _Mapping]] = ..., timestamp: _Optional[_Iterable[str]] = ..., evaluation_outputs: _Optional[_Iterable[float]] = ..., time_label: _Optional[str] = ..., output_label: _Optional[str] = ..., output_scale: _Optional[float] = ...) -> None: ...

class TSEvalInputsProto(_message.Message):
    __slots__ = ("model", "data")
    MODEL_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    model: _shared_pb2.ModelStorageInfoProto
    data: _shared_pb2.DatasetStorageInfoProto
    def __init__(self, model: _Optional[_Union[_shared_pb2.ModelStorageInfoProto, _Mapping]] = ..., data: _Optional[_Union[_shared_pb2.DatasetStorageInfoProto, _Mapping]] = ...) -> None: ...

class TSEvalOutputsProto(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class TSEvalResultProto(_message.Message):
    __slots__ = ("evaluation_outputs", "version", "timestamp", "time_label", "output_label", "output_scale")
    EVALUATION_OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TIME_LABEL_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_LABEL_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_SCALE_FIELD_NUMBER: _ClassVar[int]
    evaluation_outputs: _containers.RepeatedScalarFieldContainer[float]
    version: str
    timestamp: _containers.RepeatedScalarFieldContainer[str]
    time_label: str
    output_label: str
    output_scale: float
    def __init__(self, evaluation_outputs: _Optional[_Iterable[float]] = ..., version: _Optional[str] = ..., timestamp: _Optional[_Iterable[str]] = ..., time_label: _Optional[str] = ..., output_label: _Optional[str] = ..., output_scale: _Optional[float] = ...) -> None: ...

class TrainModelInfoProto(_message.Message):
    __slots__ = ("name", "description")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...
