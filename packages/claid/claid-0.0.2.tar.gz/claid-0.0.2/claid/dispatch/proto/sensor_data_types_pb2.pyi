from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AudioEncoding(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    ENCODING_PCM_8BIT: _ClassVar[AudioEncoding]
    ENCODING_PCM_16BIT: _ClassVar[AudioEncoding]
    ENCODING_PCM_FLOAT: _ClassVar[AudioEncoding]
    ENCODING_PCM_24_BIT_PACKED: _ClassVar[AudioEncoding]
    ENCODING_PCM_32_BIT: _ClassVar[AudioEncoding]

class AudioChannels(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    CHANNEL_MONO: _ClassVar[AudioChannels]
    CHANNEL_STEREO: _ClassVar[AudioChannels]
    CHANNEL_QUAD: _ClassVar[AudioChannels]
    CHANNEL_5POINT1: _ClassVar[AudioChannels]
    CHANNEL_7POINT1_SURROUND: _ClassVar[AudioChannels]

class BodyLocation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    left_ankle: _ClassVar[BodyLocation]
    right_ankle: _ClassVar[BodyLocation]
    left_hip: _ClassVar[BodyLocation]
    right_hip: _ClassVar[BodyLocation]
    left_thigh: _ClassVar[BodyLocation]
    right_thigh: _ClassVar[BodyLocation]
    left_thorax: _ClassVar[BodyLocation]
    middle_left_thorax: _ClassVar[BodyLocation]
    left_upper_arm: _ClassVar[BodyLocation]
    right_upper_arm: _ClassVar[BodyLocation]
    left_wrist: _ClassVar[BodyLocation]
    right_wrist: _ClassVar[BodyLocation]

class BatteryState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    UNKNOWN: _ClassVar[BatteryState]
    UNPLUGGED: _ClassVar[BatteryState]
    FULL: _ClassVar[BatteryState]
    CHARGING: _ClassVar[BatteryState]
    USB_CHARGING: _ClassVar[BatteryState]
    AC_CHARGING: _ClassVar[BatteryState]
    WIRELESS_CHARGING: _ClassVar[BatteryState]
ENCODING_PCM_8BIT: AudioEncoding
ENCODING_PCM_16BIT: AudioEncoding
ENCODING_PCM_FLOAT: AudioEncoding
ENCODING_PCM_24_BIT_PACKED: AudioEncoding
ENCODING_PCM_32_BIT: AudioEncoding
CHANNEL_MONO: AudioChannels
CHANNEL_STEREO: AudioChannels
CHANNEL_QUAD: AudioChannels
CHANNEL_5POINT1: AudioChannels
CHANNEL_7POINT1_SURROUND: AudioChannels
left_ankle: BodyLocation
right_ankle: BodyLocation
left_hip: BodyLocation
right_hip: BodyLocation
left_thigh: BodyLocation
right_thigh: BodyLocation
left_thorax: BodyLocation
middle_left_thorax: BodyLocation
left_upper_arm: BodyLocation
right_upper_arm: BodyLocation
left_wrist: BodyLocation
right_wrist: BodyLocation
UNKNOWN: BatteryState
UNPLUGGED: BatteryState
FULL: BatteryState
CHARGING: BatteryState
USB_CHARGING: BatteryState
AC_CHARGING: BatteryState
WIRELESS_CHARGING: BatteryState

class AudioData(_message.Message):
    __slots__ = ["data", "sampling_rate", "bit_rate", "encoding", "channels"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    SAMPLING_RATE_FIELD_NUMBER: _ClassVar[int]
    BIT_RATE_FIELD_NUMBER: _ClassVar[int]
    ENCODING_FIELD_NUMBER: _ClassVar[int]
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    sampling_rate: int
    bit_rate: int
    encoding: AudioEncoding
    channels: AudioChannels
    def __init__(self, data: _Optional[bytes] = ..., sampling_rate: _Optional[int] = ..., bit_rate: _Optional[int] = ..., encoding: _Optional[_Union[AudioEncoding, str]] = ..., channels: _Optional[_Union[AudioChannels, str]] = ...) -> None: ...

class AccelerationUnitValue(_message.Message):
    __slots__ = ["unit", "value"]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    unit: str
    value: float
    def __init__(self, unit: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...

class ActivityName(_message.Message):
    __slots__ = ["type"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    type: str
    def __init__(self, type: _Optional[str] = ...) -> None: ...

class AccelerationSample(_message.Message):
    __slots__ = ["acceleration_x", "acceleration_y", "acceleration_z", "sensor_body_location", "unix_timestamp_in_ms", "effective_time_frame"]
    ACCELERATION_X_FIELD_NUMBER: _ClassVar[int]
    ACCELERATION_Y_FIELD_NUMBER: _ClassVar[int]
    ACCELERATION_Z_FIELD_NUMBER: _ClassVar[int]
    SENSOR_BODY_LOCATION_FIELD_NUMBER: _ClassVar[int]
    UNIX_TIMESTAMP_IN_MS_FIELD_NUMBER: _ClassVar[int]
    EFFECTIVE_TIME_FRAME_FIELD_NUMBER: _ClassVar[int]
    acceleration_x: float
    acceleration_y: float
    acceleration_z: float
    sensor_body_location: str
    unix_timestamp_in_ms: int
    effective_time_frame: str
    def __init__(self, acceleration_x: _Optional[float] = ..., acceleration_y: _Optional[float] = ..., acceleration_z: _Optional[float] = ..., sensor_body_location: _Optional[str] = ..., unix_timestamp_in_ms: _Optional[int] = ..., effective_time_frame: _Optional[str] = ...) -> None: ...

class AccelerationData(_message.Message):
    __slots__ = ["samples"]
    SAMPLES_FIELD_NUMBER: _ClassVar[int]
    samples: _containers.RepeatedCompositeFieldContainer[AccelerationSample]
    def __init__(self, samples: _Optional[_Iterable[_Union[AccelerationSample, _Mapping]]] = ...) -> None: ...

class GyroscopeSample(_message.Message):
    __slots__ = ["gyroscope_x", "gyroscope_y", "gyroscope_z", "sensor_body_location", "unix_timestamp_in_ms", "effective_time_frame"]
    GYROSCOPE_X_FIELD_NUMBER: _ClassVar[int]
    GYROSCOPE_Y_FIELD_NUMBER: _ClassVar[int]
    GYROSCOPE_Z_FIELD_NUMBER: _ClassVar[int]
    SENSOR_BODY_LOCATION_FIELD_NUMBER: _ClassVar[int]
    UNIX_TIMESTAMP_IN_MS_FIELD_NUMBER: _ClassVar[int]
    EFFECTIVE_TIME_FRAME_FIELD_NUMBER: _ClassVar[int]
    gyroscope_x: float
    gyroscope_y: float
    gyroscope_z: float
    sensor_body_location: str
    unix_timestamp_in_ms: int
    effective_time_frame: str
    def __init__(self, gyroscope_x: _Optional[float] = ..., gyroscope_y: _Optional[float] = ..., gyroscope_z: _Optional[float] = ..., sensor_body_location: _Optional[str] = ..., unix_timestamp_in_ms: _Optional[int] = ..., effective_time_frame: _Optional[str] = ...) -> None: ...

class GyroscopeData(_message.Message):
    __slots__ = ["samples"]
    SAMPLES_FIELD_NUMBER: _ClassVar[int]
    samples: _containers.RepeatedCompositeFieldContainer[GyroscopeSample]
    def __init__(self, samples: _Optional[_Iterable[_Union[GyroscopeSample, _Mapping]]] = ...) -> None: ...

class HeartRateSample(_message.Message):
    __slots__ = ["hr", "hrInterBeatInterval", "status", "unix_timestamp_in_ms"]
    HR_FIELD_NUMBER: _ClassVar[int]
    HRINTERBEATINTERVAL_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    UNIX_TIMESTAMP_IN_MS_FIELD_NUMBER: _ClassVar[int]
    hr: int
    hrInterBeatInterval: int
    status: int
    unix_timestamp_in_ms: int
    def __init__(self, hr: _Optional[int] = ..., hrInterBeatInterval: _Optional[int] = ..., status: _Optional[int] = ..., unix_timestamp_in_ms: _Optional[int] = ...) -> None: ...

class HeartRateData(_message.Message):
    __slots__ = ["samples"]
    SAMPLES_FIELD_NUMBER: _ClassVar[int]
    samples: _containers.RepeatedCompositeFieldContainer[HeartRateSample]
    def __init__(self, samples: _Optional[_Iterable[_Union[HeartRateSample, _Mapping]]] = ...) -> None: ...

class BatterySample(_message.Message):
    __slots__ = ["level", "state", "unix_timestamp_in_ms"]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    UNIX_TIMESTAMP_IN_MS_FIELD_NUMBER: _ClassVar[int]
    level: int
    state: BatteryState
    unix_timestamp_in_ms: int
    def __init__(self, level: _Optional[int] = ..., state: _Optional[_Union[BatteryState, str]] = ..., unix_timestamp_in_ms: _Optional[int] = ...) -> None: ...

class BatteryData(_message.Message):
    __slots__ = ["samples"]
    SAMPLES_FIELD_NUMBER: _ClassVar[int]
    samples: _containers.RepeatedCompositeFieldContainer[BatterySample]
    def __init__(self, samples: _Optional[_Iterable[_Union[BatterySample, _Mapping]]] = ...) -> None: ...
