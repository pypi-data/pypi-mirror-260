from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CtrlType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    CTRL_UNSPECIFIED: _ClassVar[CtrlType]
    CTRL_RUNTIME_PING: _ClassVar[CtrlType]
    CTRL_REMOTE_PING: _ClassVar[CtrlType]
    CTRL_REMOTE_PING_PONG: _ClassVar[CtrlType]
    CTRL_CONN_CANCEL: _ClassVar[CtrlType]
    CTRL_ERROR: _ClassVar[CtrlType]
    CTRL_CONNECTED_TO_REMOTE_SERVER: _ClassVar[CtrlType]
    CTRL_DISCONNECTED_FROM_REMOTE_SERVER: _ClassVar[CtrlType]
    CTRL_UNLOAD_MODULES: _ClassVar[CtrlType]
    CTRL_UNLOAD_MODULES_DONE: _ClassVar[CtrlType]
    CTRL_RESTART_RUNTIME: _ClassVar[CtrlType]
    CTRL_RESTART_RUNTIME_DONE: _ClassVar[CtrlType]
    CTRL_REQUEST_MODULE_ANNOTATIONS: _ClassVar[CtrlType]
    CTRL_REQUEST_MODULE_ANNOTATIONS_RESPONSE: _ClassVar[CtrlType]
    CTRL_UPLOAD_CONFIG_AND_DATA: _ClassVar[CtrlType]
    CTRL_ON_NEW_CONFIG_PAYLOAD_DATA: _ClassVar[CtrlType]
    CTRL_LOCAL_LOG_MESSAGE: _ClassVar[CtrlType]
    CTRL_LOG_SINK_LOG_MESSAGE_STREAM: _ClassVar[CtrlType]
    CTRL_SUBSCRIBE_TO_LOG_SINK_LOG_MESSAGE_STREAM: _ClassVar[CtrlType]
    CTRL_UNSUBSCRIBE_FROM_LOG_SINK_LOG_MESSAGE_STREAM: _ClassVar[CtrlType]

class Codec(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    CODEC_UNSPECIFIED: _ClassVar[Codec]
    CODEC_BYTES: _ClassVar[Codec]
    CODEC_FILE: _ClassVar[Codec]
    CODEC_JSON: _ClassVar[Codec]
    CODEC_PROTO: _ClassVar[Codec]

class PropertyType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    PROPERTY_TYPE_DEFAULT: _ClassVar[PropertyType]
    PROPERTY_TYPE_ENUM: _ClassVar[PropertyType]

class Runtime(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    RUNTIME_UNSPECIFIED: _ClassVar[Runtime]
    RUNTIME_CPP: _ClassVar[Runtime]
    RUNTIME_DART: _ClassVar[Runtime]
    RUNTIME_JAVA: _ClassVar[Runtime]
    RUNTIME_PYTHON: _ClassVar[Runtime]

class LogMessageSeverityLevel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    DEBUG_VERBOSE: _ClassVar[LogMessageSeverityLevel]
    INFO: _ClassVar[LogMessageSeverityLevel]
    WARNING: _ClassVar[LogMessageSeverityLevel]
    ERROR: _ClassVar[LogMessageSeverityLevel]
    FATAL: _ClassVar[LogMessageSeverityLevel]

class LogMessageEntityType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    MIDDLEWARE: _ClassVar[LogMessageEntityType]
    MIDDLEWARE_COMPONENT: _ClassVar[LogMessageEntityType]
    MODULE: _ClassVar[LogMessageEntityType]

class LogSinkTransferMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    STORE_AND_UPLOAD: _ClassVar[LogSinkTransferMode]
    STREAM: _ClassVar[LogSinkTransferMode]
CTRL_UNSPECIFIED: CtrlType
CTRL_RUNTIME_PING: CtrlType
CTRL_REMOTE_PING: CtrlType
CTRL_REMOTE_PING_PONG: CtrlType
CTRL_CONN_CANCEL: CtrlType
CTRL_ERROR: CtrlType
CTRL_CONNECTED_TO_REMOTE_SERVER: CtrlType
CTRL_DISCONNECTED_FROM_REMOTE_SERVER: CtrlType
CTRL_UNLOAD_MODULES: CtrlType
CTRL_UNLOAD_MODULES_DONE: CtrlType
CTRL_RESTART_RUNTIME: CtrlType
CTRL_RESTART_RUNTIME_DONE: CtrlType
CTRL_REQUEST_MODULE_ANNOTATIONS: CtrlType
CTRL_REQUEST_MODULE_ANNOTATIONS_RESPONSE: CtrlType
CTRL_UPLOAD_CONFIG_AND_DATA: CtrlType
CTRL_ON_NEW_CONFIG_PAYLOAD_DATA: CtrlType
CTRL_LOCAL_LOG_MESSAGE: CtrlType
CTRL_LOG_SINK_LOG_MESSAGE_STREAM: CtrlType
CTRL_SUBSCRIBE_TO_LOG_SINK_LOG_MESSAGE_STREAM: CtrlType
CTRL_UNSUBSCRIBE_FROM_LOG_SINK_LOG_MESSAGE_STREAM: CtrlType
CODEC_UNSPECIFIED: Codec
CODEC_BYTES: Codec
CODEC_FILE: Codec
CODEC_JSON: Codec
CODEC_PROTO: Codec
PROPERTY_TYPE_DEFAULT: PropertyType
PROPERTY_TYPE_ENUM: PropertyType
RUNTIME_UNSPECIFIED: Runtime
RUNTIME_CPP: Runtime
RUNTIME_DART: Runtime
RUNTIME_JAVA: Runtime
RUNTIME_PYTHON: Runtime
DEBUG_VERBOSE: LogMessageSeverityLevel
INFO: LogMessageSeverityLevel
WARNING: LogMessageSeverityLevel
ERROR: LogMessageSeverityLevel
FATAL: LogMessageSeverityLevel
MIDDLEWARE: LogMessageEntityType
MIDDLEWARE_COMPONENT: LogMessageEntityType
MODULE: LogMessageEntityType
STORE_AND_UPLOAD: LogSinkTransferMode
STREAM: LogSinkTransferMode

class DataPackage(_message.Message):
    __slots__ = ["id", "channel", "source_module", "target_module", "source_host", "target_host", "source_user_token", "target_user_token", "device_id", "trace_points", "unix_timestamp_ms", "control_val", "number_val", "string_val", "bool_val", "number_array_val", "string_array_val", "number_map", "string_map", "blob_val"]
    ID_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    SOURCE_MODULE_FIELD_NUMBER: _ClassVar[int]
    TARGET_MODULE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_HOST_FIELD_NUMBER: _ClassVar[int]
    TARGET_HOST_FIELD_NUMBER: _ClassVar[int]
    SOURCE_USER_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TARGET_USER_TOKEN_FIELD_NUMBER: _ClassVar[int]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    TRACE_POINTS_FIELD_NUMBER: _ClassVar[int]
    UNIX_TIMESTAMP_MS_FIELD_NUMBER: _ClassVar[int]
    CONTROL_VAL_FIELD_NUMBER: _ClassVar[int]
    NUMBER_VAL_FIELD_NUMBER: _ClassVar[int]
    STRING_VAL_FIELD_NUMBER: _ClassVar[int]
    BOOL_VAL_FIELD_NUMBER: _ClassVar[int]
    NUMBER_ARRAY_VAL_FIELD_NUMBER: _ClassVar[int]
    STRING_ARRAY_VAL_FIELD_NUMBER: _ClassVar[int]
    NUMBER_MAP_FIELD_NUMBER: _ClassVar[int]
    STRING_MAP_FIELD_NUMBER: _ClassVar[int]
    BLOB_VAL_FIELD_NUMBER: _ClassVar[int]
    id: str
    channel: str
    source_module: str
    target_module: str
    source_host: str
    target_host: str
    source_user_token: str
    target_user_token: str
    device_id: str
    trace_points: _containers.RepeatedCompositeFieldContainer[TracePoint]
    unix_timestamp_ms: int
    control_val: ControlPackage
    number_val: float
    string_val: str
    bool_val: bool
    number_array_val: NumberArray
    string_array_val: StringArray
    number_map: NumberMap
    string_map: StringMap
    blob_val: Blob
    def __init__(self, id: _Optional[str] = ..., channel: _Optional[str] = ..., source_module: _Optional[str] = ..., target_module: _Optional[str] = ..., source_host: _Optional[str] = ..., target_host: _Optional[str] = ..., source_user_token: _Optional[str] = ..., target_user_token: _Optional[str] = ..., device_id: _Optional[str] = ..., trace_points: _Optional[_Iterable[_Union[TracePoint, _Mapping]]] = ..., unix_timestamp_ms: _Optional[int] = ..., control_val: _Optional[_Union[ControlPackage, _Mapping]] = ..., number_val: _Optional[float] = ..., string_val: _Optional[str] = ..., bool_val: bool = ..., number_array_val: _Optional[_Union[NumberArray, _Mapping]] = ..., string_array_val: _Optional[_Union[StringArray, _Mapping]] = ..., number_map: _Optional[_Union[NumberMap, _Mapping]] = ..., string_map: _Optional[_Union[StringMap, _Mapping]] = ..., blob_val: _Optional[_Union[Blob, _Mapping]] = ...) -> None: ...

class ControlPackage(_message.Message):
    __slots__ = ["ctrl_type", "runtime", "remote_client_info", "status", "error_msg", "action_request", "module_annotations", "config_upload_payload", "log_message"]
    class ModuleAnnotationsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ModuleAnnotation
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ModuleAnnotation, _Mapping]] = ...) -> None: ...
    CTRL_TYPE_FIELD_NUMBER: _ClassVar[int]
    RUNTIME_FIELD_NUMBER: _ClassVar[int]
    REMOTE_CLIENT_INFO_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MSG_FIELD_NUMBER: _ClassVar[int]
    ACTION_REQUEST_FIELD_NUMBER: _ClassVar[int]
    MODULE_ANNOTATIONS_FIELD_NUMBER: _ClassVar[int]
    CONFIG_UPLOAD_PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    LOG_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ctrl_type: CtrlType
    runtime: Runtime
    remote_client_info: RemoteClientInfo
    status: AccumulatedStatus
    error_msg: ErrorMsg
    action_request: ActionRequest
    module_annotations: _containers.MessageMap[str, ModuleAnnotation]
    config_upload_payload: ConfigUploadPayload
    log_message: LogMessage
    def __init__(self, ctrl_type: _Optional[_Union[CtrlType, str]] = ..., runtime: _Optional[_Union[Runtime, str]] = ..., remote_client_info: _Optional[_Union[RemoteClientInfo, _Mapping]] = ..., status: _Optional[_Union[AccumulatedStatus, _Mapping]] = ..., error_msg: _Optional[_Union[ErrorMsg, _Mapping]] = ..., action_request: _Optional[_Union[ActionRequest, _Mapping]] = ..., module_annotations: _Optional[_Mapping[str, ModuleAnnotation]] = ..., config_upload_payload: _Optional[_Union[ConfigUploadPayload, _Mapping]] = ..., log_message: _Optional[_Union[LogMessage, _Mapping]] = ...) -> None: ...

class AccumulatedStatus(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ErrorMsg(_message.Message):
    __slots__ = ["message", "cancel"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CANCEL_FIELD_NUMBER: _ClassVar[int]
    message: str
    cancel: bool
    def __init__(self, message: _Optional[str] = ..., cancel: bool = ...) -> None: ...

class ActionRequest(_message.Message):
    __slots__ = ["action_params"]
    class ActionParamsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ACTION_PARAMS_FIELD_NUMBER: _ClassVar[int]
    action_params: _containers.ScalarMap[str, str]
    def __init__(self, action_params: _Optional[_Mapping[str, str]] = ...) -> None: ...

class NumberArray(_message.Message):
    __slots__ = ["val"]
    VAL_FIELD_NUMBER: _ClassVar[int]
    val: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, val: _Optional[_Iterable[float]] = ...) -> None: ...

class StringArray(_message.Message):
    __slots__ = ["val"]
    VAL_FIELD_NUMBER: _ClassVar[int]
    val: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, val: _Optional[_Iterable[str]] = ...) -> None: ...

class NumberMap(_message.Message):
    __slots__ = ["val"]
    class ValEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    VAL_FIELD_NUMBER: _ClassVar[int]
    val: _containers.ScalarMap[str, float]
    def __init__(self, val: _Optional[_Mapping[str, float]] = ...) -> None: ...

class StringMap(_message.Message):
    __slots__ = ["val"]
    class ValEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    VAL_FIELD_NUMBER: _ClassVar[int]
    val: _containers.ScalarMap[str, str]
    def __init__(self, val: _Optional[_Mapping[str, str]] = ...) -> None: ...

class Blob(_message.Message):
    __slots__ = ["codec", "payload", "name", "message_type", "sub_type"]
    CODEC_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SUB_TYPE_FIELD_NUMBER: _ClassVar[int]
    codec: Codec
    payload: bytes
    name: str
    message_type: str
    sub_type: str
    def __init__(self, codec: _Optional[_Union[Codec, str]] = ..., payload: _Optional[bytes] = ..., name: _Optional[str] = ..., message_type: _Optional[str] = ..., sub_type: _Optional[str] = ...) -> None: ...

class TracePoint(_message.Message):
    __slots__ = ["time_stamp", "node_id"]
    TIME_STAMP_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    time_stamp: _timestamp_pb2.Timestamp
    node_id: str
    def __init__(self, time_stamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., node_id: _Optional[str] = ...) -> None: ...

class ModuleListRequest(_message.Message):
    __slots__ = ["runtime", "supported_module_classes", "module_annotations"]
    class ModuleAnnotationsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ModuleAnnotation
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ModuleAnnotation, _Mapping]] = ...) -> None: ...
    RUNTIME_FIELD_NUMBER: _ClassVar[int]
    SUPPORTED_MODULE_CLASSES_FIELD_NUMBER: _ClassVar[int]
    MODULE_ANNOTATIONS_FIELD_NUMBER: _ClassVar[int]
    runtime: Runtime
    supported_module_classes: _containers.RepeatedScalarFieldContainer[str]
    module_annotations: _containers.MessageMap[str, ModuleAnnotation]
    def __init__(self, runtime: _Optional[_Union[Runtime, str]] = ..., supported_module_classes: _Optional[_Iterable[str]] = ..., module_annotations: _Optional[_Mapping[str, ModuleAnnotation]] = ...) -> None: ...

class ModuleListResponse(_message.Message):
    __slots__ = ["descriptors"]
    class ModuleDescriptor(_message.Message):
        __slots__ = ["module_id", "module_class", "properties"]
        class PropertiesEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: str
            def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
        MODULE_ID_FIELD_NUMBER: _ClassVar[int]
        MODULE_CLASS_FIELD_NUMBER: _ClassVar[int]
        PROPERTIES_FIELD_NUMBER: _ClassVar[int]
        module_id: str
        module_class: str
        properties: _containers.ScalarMap[str, str]
        def __init__(self, module_id: _Optional[str] = ..., module_class: _Optional[str] = ..., properties: _Optional[_Mapping[str, str]] = ...) -> None: ...
    DESCRIPTORS_FIELD_NUMBER: _ClassVar[int]
    descriptors: _containers.RepeatedCompositeFieldContainer[ModuleListResponse.ModuleDescriptor]
    def __init__(self, descriptors: _Optional[_Iterable[_Union[ModuleListResponse.ModuleDescriptor, _Mapping]]] = ...) -> None: ...

class InitRuntimeRequest(_message.Message):
    __slots__ = ["runtime", "modules"]
    class ModuleChannels(_message.Message):
        __slots__ = ["module_id", "channel_packets"]
        MODULE_ID_FIELD_NUMBER: _ClassVar[int]
        CHANNEL_PACKETS_FIELD_NUMBER: _ClassVar[int]
        module_id: str
        channel_packets: _containers.RepeatedCompositeFieldContainer[DataPackage]
        def __init__(self, module_id: _Optional[str] = ..., channel_packets: _Optional[_Iterable[_Union[DataPackage, _Mapping]]] = ...) -> None: ...
    RUNTIME_FIELD_NUMBER: _ClassVar[int]
    MODULES_FIELD_NUMBER: _ClassVar[int]
    runtime: Runtime
    modules: _containers.RepeatedCompositeFieldContainer[InitRuntimeRequest.ModuleChannels]
    def __init__(self, runtime: _Optional[_Union[Runtime, str]] = ..., modules: _Optional[_Iterable[_Union[InitRuntimeRequest.ModuleChannels, _Mapping]]] = ...) -> None: ...

class RemoteClientInfo(_message.Message):
    __slots__ = ["host", "user_token", "device_id"]
    HOST_FIELD_NUMBER: _ClassVar[int]
    USER_TOKEN_FIELD_NUMBER: _ClassVar[int]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    host: str
    user_token: str
    device_id: str
    def __init__(self, host: _Optional[str] = ..., user_token: _Optional[str] = ..., device_id: _Optional[str] = ...) -> None: ...

class AddModuleRequest(_message.Message):
    __slots__ = ["module_id", "module_class", "properties", "channel_packets"]
    class PropertiesEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    MODULE_ID_FIELD_NUMBER: _ClassVar[int]
    MODULE_CLASS_FIELD_NUMBER: _ClassVar[int]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_PACKETS_FIELD_NUMBER: _ClassVar[int]
    module_id: str
    module_class: str
    properties: _containers.ScalarMap[str, str]
    channel_packets: _containers.RepeatedCompositeFieldContainer[DataPackage]
    def __init__(self, module_id: _Optional[str] = ..., module_class: _Optional[str] = ..., properties: _Optional[_Mapping[str, str]] = ..., channel_packets: _Optional[_Iterable[_Union[DataPackage, _Mapping]]] = ...) -> None: ...

class RemoveModuleRequest(_message.Message):
    __slots__ = ["module_id"]
    MODULE_ID_FIELD_NUMBER: _ClassVar[int]
    module_id: str
    def __init__(self, module_id: _Optional[str] = ...) -> None: ...

class PropertyHint(_message.Message):
    __slots__ = ["property_type", "property_type_enum_values"]
    PROPERTY_TYPE_FIELD_NUMBER: _ClassVar[int]
    PROPERTY_TYPE_ENUM_VALUES_FIELD_NUMBER: _ClassVar[int]
    property_type: PropertyType
    property_type_enum_values: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, property_type: _Optional[_Union[PropertyType, str]] = ..., property_type_enum_values: _Optional[_Iterable[str]] = ...) -> None: ...

class ModuleAnnotation(_message.Message):
    __slots__ = ["module_description", "module_category", "properties", "property_descriptions", "property_hints", "channel_definition", "channel_description"]
    MODULE_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    MODULE_CATEGORY_FIELD_NUMBER: _ClassVar[int]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    PROPERTY_DESCRIPTIONS_FIELD_NUMBER: _ClassVar[int]
    PROPERTY_HINTS_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_DEFINITION_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    module_description: str
    module_category: str
    properties: _containers.RepeatedScalarFieldContainer[str]
    property_descriptions: _containers.RepeatedScalarFieldContainer[str]
    property_hints: _containers.RepeatedCompositeFieldContainer[PropertyHint]
    channel_definition: _containers.RepeatedCompositeFieldContainer[DataPackage]
    channel_description: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, module_description: _Optional[str] = ..., module_category: _Optional[str] = ..., properties: _Optional[_Iterable[str]] = ..., property_descriptions: _Optional[_Iterable[str]] = ..., property_hints: _Optional[_Iterable[_Union[PropertyHint, _Mapping]]] = ..., channel_definition: _Optional[_Iterable[_Union[DataPackage, _Mapping]]] = ..., channel_description: _Optional[_Iterable[str]] = ...) -> None: ...

class LogMessage(_message.Message):
    __slots__ = ["log_message", "severity_level", "unix_timestamp_in_ms", "entity_type", "entity_name", "runtime"]
    LOG_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_LEVEL_FIELD_NUMBER: _ClassVar[int]
    UNIX_TIMESTAMP_IN_MS_FIELD_NUMBER: _ClassVar[int]
    ENTITY_TYPE_FIELD_NUMBER: _ClassVar[int]
    ENTITY_NAME_FIELD_NUMBER: _ClassVar[int]
    RUNTIME_FIELD_NUMBER: _ClassVar[int]
    log_message: str
    severity_level: LogMessageSeverityLevel
    unix_timestamp_in_ms: int
    entity_type: LogMessageEntityType
    entity_name: str
    runtime: Runtime
    def __init__(self, log_message: _Optional[str] = ..., severity_level: _Optional[_Union[LogMessageSeverityLevel, str]] = ..., unix_timestamp_in_ms: _Optional[int] = ..., entity_type: _Optional[_Union[LogMessageEntityType, str]] = ..., entity_name: _Optional[str] = ..., runtime: _Optional[_Union[Runtime, str]] = ...) -> None: ...

class CLAIDConfig(_message.Message):
    __slots__ = ["hosts", "log_sink_host", "log_sink_severity_level", "log_sink_transfer_mode", "log_sink_log_storage_path"]
    HOSTS_FIELD_NUMBER: _ClassVar[int]
    LOG_SINK_HOST_FIELD_NUMBER: _ClassVar[int]
    LOG_SINK_SEVERITY_LEVEL_FIELD_NUMBER: _ClassVar[int]
    LOG_SINK_TRANSFER_MODE_FIELD_NUMBER: _ClassVar[int]
    LOG_SINK_LOG_STORAGE_PATH_FIELD_NUMBER: _ClassVar[int]
    hosts: _containers.RepeatedCompositeFieldContainer[HostConfig]
    log_sink_host: str
    log_sink_severity_level: LogMessageSeverityLevel
    log_sink_transfer_mode: LogSinkTransferMode
    log_sink_log_storage_path: str
    def __init__(self, hosts: _Optional[_Iterable[_Union[HostConfig, _Mapping]]] = ..., log_sink_host: _Optional[str] = ..., log_sink_severity_level: _Optional[_Union[LogMessageSeverityLevel, str]] = ..., log_sink_transfer_mode: _Optional[_Union[LogSinkTransferMode, str]] = ..., log_sink_log_storage_path: _Optional[str] = ...) -> None: ...

class HostConfig(_message.Message):
    __slots__ = ["hostname", "type", "is_server", "host_server_address", "connect_to", "modules", "log_folder", "min_log_severity_level"]
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    IS_SERVER_FIELD_NUMBER: _ClassVar[int]
    HOST_SERVER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    CONNECT_TO_FIELD_NUMBER: _ClassVar[int]
    MODULES_FIELD_NUMBER: _ClassVar[int]
    LOG_FOLDER_FIELD_NUMBER: _ClassVar[int]
    MIN_LOG_SEVERITY_LEVEL_FIELD_NUMBER: _ClassVar[int]
    hostname: str
    type: str
    is_server: bool
    host_server_address: str
    connect_to: str
    modules: _containers.RepeatedCompositeFieldContainer[ModuleConfig]
    log_folder: str
    min_log_severity_level: LogMessageSeverityLevel
    def __init__(self, hostname: _Optional[str] = ..., type: _Optional[str] = ..., is_server: bool = ..., host_server_address: _Optional[str] = ..., connect_to: _Optional[str] = ..., modules: _Optional[_Iterable[_Union[ModuleConfig, _Mapping]]] = ..., log_folder: _Optional[str] = ..., min_log_severity_level: _Optional[_Union[LogMessageSeverityLevel, str]] = ...) -> None: ...

class ModuleConfig(_message.Message):
    __slots__ = ["id", "type", "input_channels", "output_channels", "properties"]
    class InputChannelsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class OutputChannelsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class PropertiesEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    INPUT_CHANNELS_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_CHANNELS_FIELD_NUMBER: _ClassVar[int]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    id: str
    type: str
    input_channels: _containers.ScalarMap[str, str]
    output_channels: _containers.ScalarMap[str, str]
    properties: _containers.ScalarMap[str, str]
    def __init__(self, id: _Optional[str] = ..., type: _Optional[str] = ..., input_channels: _Optional[_Mapping[str, str]] = ..., output_channels: _Optional[_Mapping[str, str]] = ..., properties: _Optional[_Mapping[str, str]] = ...) -> None: ...

class DataFile(_message.Message):
    __slots__ = ["relative_path", "file_data"]
    RELATIVE_PATH_FIELD_NUMBER: _ClassVar[int]
    FILE_DATA_FIELD_NUMBER: _ClassVar[int]
    relative_path: str
    file_data: bytes
    def __init__(self, relative_path: _Optional[str] = ..., file_data: _Optional[bytes] = ...) -> None: ...

class ModuleInjectionDescription(_message.Message):
    __slots__ = ["module_name", "module_file", "runtime"]
    MODULE_NAME_FIELD_NUMBER: _ClassVar[int]
    MODULE_FILE_FIELD_NUMBER: _ClassVar[int]
    RUNTIME_FIELD_NUMBER: _ClassVar[int]
    module_name: str
    module_file: str
    runtime: Runtime
    def __init__(self, module_name: _Optional[str] = ..., module_file: _Optional[str] = ..., runtime: _Optional[_Union[Runtime, str]] = ...) -> None: ...

class ConfigUploadPayload(_message.Message):
    __slots__ = ["config", "payload_files", "modules_to_inject", "payload_data_path"]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FILES_FIELD_NUMBER: _ClassVar[int]
    MODULES_TO_INJECT_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_DATA_PATH_FIELD_NUMBER: _ClassVar[int]
    config: CLAIDConfig
    payload_files: _containers.RepeatedCompositeFieldContainer[DataFile]
    modules_to_inject: _containers.RepeatedCompositeFieldContainer[ModuleInjectionDescription]
    payload_data_path: str
    def __init__(self, config: _Optional[_Union[CLAIDConfig, _Mapping]] = ..., payload_files: _Optional[_Iterable[_Union[DataFile, _Mapping]]] = ..., modules_to_inject: _Optional[_Iterable[_Union[ModuleInjectionDescription, _Mapping]]] = ..., payload_data_path: _Optional[str] = ...) -> None: ...
