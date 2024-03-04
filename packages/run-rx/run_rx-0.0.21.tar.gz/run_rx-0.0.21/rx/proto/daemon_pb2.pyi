from google.protobuf import empty_pb2 as _empty_pb2
from rx.proto import rx_pb2 as _rx_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ClosePortRequest(_message.Message):
    __slots__ = ["port"]
    PORT_FIELD_NUMBER: _ClassVar[int]
    port: int
    def __init__(self, port: _Optional[int] = ...) -> None: ...

class GetPortsResponse(_message.Message):
    __slots__ = ["ports", "result"]
    class Port(_message.Message):
        __slots__ = ["local_port", "port"]
        LOCAL_PORT_FIELD_NUMBER: _ClassVar[int]
        PORT_FIELD_NUMBER: _ClassVar[int]
        local_port: int
        port: int
        def __init__(self, port: _Optional[int] = ..., local_port: _Optional[int] = ...) -> None: ...
    PORTS_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    ports: _containers.RepeatedCompositeFieldContainer[GetPortsResponse.Port]
    result: _rx_pb2.Result
    def __init__(self, result: _Optional[_Union[_rx_pb2.Result, _Mapping]] = ..., ports: _Optional[_Iterable[_Union[GetPortsResponse.Port, _Mapping]]] = ...) -> None: ...

class OpenPortRequest(_message.Message):
    __slots__ = ["local_port", "port"]
    LOCAL_PORT_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    local_port: int
    port: int
    def __init__(self, port: _Optional[int] = ..., local_port: _Optional[int] = ...) -> None: ...
