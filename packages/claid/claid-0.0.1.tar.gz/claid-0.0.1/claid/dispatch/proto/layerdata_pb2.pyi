from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LayerDataType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    INT8: _ClassVar[LayerDataType]
    UINT8: _ClassVar[LayerDataType]
    INT16: _ClassVar[LayerDataType]
    UINT16: _ClassVar[LayerDataType]
    INT32: _ClassVar[LayerDataType]
    UINT32: _ClassVar[LayerDataType]
    FLOAT32: _ClassVar[LayerDataType]

class LayerDataOrder(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    NCHW: _ClassVar[LayerDataOrder]
    NHWC: _ClassVar[LayerDataOrder]
    CHW: _ClassVar[LayerDataOrder]
    HWC: _ClassVar[LayerDataOrder]
    NW: _ClassVar[LayerDataOrder]
INT8: LayerDataType
UINT8: LayerDataType
INT16: LayerDataType
UINT16: LayerDataType
INT32: LayerDataType
UINT32: LayerDataType
FLOAT32: LayerDataType
NCHW: LayerDataOrder
NHWC: LayerDataOrder
CHW: LayerDataOrder
HWC: LayerDataOrder
NW: LayerDataOrder

class LayerDimension(_message.Message):
    __slots__ = ["numBatches", "height", "width", "channels"]
    NUMBATCHES_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    numBatches: int
    height: int
    width: int
    channels: int
    def __init__(self, numBatches: _Optional[int] = ..., height: _Optional[int] = ..., width: _Optional[int] = ..., channels: _Optional[int] = ...) -> None: ...

class LayerData(_message.Message):
    __slots__ = ["data", "layer_name", "layer_dimension", "data_type", "data_order"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    LAYER_NAME_FIELD_NUMBER: _ClassVar[int]
    LAYER_DIMENSION_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    DATA_ORDER_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    layer_name: str
    layer_dimension: LayerDimension
    data_type: LayerDataType
    data_order: LayerDataOrder
    def __init__(self, data: _Optional[bytes] = ..., layer_name: _Optional[str] = ..., layer_dimension: _Optional[_Union[LayerDimension, _Mapping]] = ..., data_type: _Optional[_Union[LayerDataType, str]] = ..., data_order: _Optional[_Union[LayerDataOrder, str]] = ...) -> None: ...

class LayerDataVector(_message.Message):
    __slots__ = ["layers"]
    LAYERS_FIELD_NUMBER: _ClassVar[int]
    layers: _containers.RepeatedCompositeFieldContainer[LayerData]
    def __init__(self, layers: _Optional[_Iterable[_Union[LayerData, _Mapping]]] = ...) -> None: ...
