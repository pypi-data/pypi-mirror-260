from typing import Any, Iterable
from .errors import InvalidEncodingError, InvalidErrorsError, InvalidValueError


class BufferReadable:
    def __instancecheck__(self, __instance: Any) -> bool:
        if isinstance(__instance, (str, bytes, bytearray)):
            return True
        return False
    

class Helpers:
    @staticmethod
    def __params_to_bytelike(
        __o: BufferReadable, encoding: str='utf-8', errors: str='strict',
        array: bool=False
    ) -> bytes:
        if array:
            return bytearray(__o, encoding, errors)
        return bytes(__o, encoding, errors)

    @staticmethod
    def __get_params(*args, **kwargs) -> tuple[str, str]:
        encoding = kwargs.get('encoding', 'utf-8')
        errors = kwargs.get('errors', 'strict')
        if args:
            if len(args) >= 1:
                encoding = args[0]
            if len(args) >= 2:
                errors = args[1]
        return (encoding, errors)
    
    @staticmethod
    def __valid_iter_item(__o: object) -> bool:
        return isinstance(__o, int) and __o >= 0 and __o < 256

    @classmethod
    def __iter_bytelike(
        cls, __o: Iterable, encoding: str='utf-8', errors: str='strict', 
        array: bool=False
    ) -> bytes:
        if all(cls.__valid_iter_item(x) for x in __o):
            return cls.__params_to_bytelike(
                __o, encoding, errors, array
            )
        invalids = (__o, [Iterable])
        raise InvalidValueError(invalids, bytes)
    
    @classmethod
    def __to_bytelike(
        cls, __o: BufferReadable | int | Iterable=None, array: bool=False, 
        *args, **kwargs
    ) -> bytes | bytearray:
        if __o is None:
            if array:
                return bytearray()
            return b''
        encoding, errors = cls.__get_params(*args, **kwargs)
        if not isinstance(encoding, str):
            raise InvalidEncodingError(encoding, bytes)
        if not isinstance(errors, str):
            raise InvalidErrorsError(errors, bytes)
        if isinstance(__o, (BufferReadable, int)):
            return cls.__params_to_bytelike(__o, encoding, errors, array)
        if isinstance(__o, Iterable):
            return cls.__iter_bytelike(__o, encoding, errors, array)
        invalids = (__o, [BufferReadable, int, Iterable])
        raise InvalidValueError(invalids)


def to_bytes(
    __o: BufferReadable | int | Iterable=None, *args, **kwargs
) -> bytes:
    byte = Helpers.__to_bytelike(__o, False, *args, **kwargs)
    return byte

def to_bytearray(
    __o: BufferReadable | int | Iterable=None, *args, **kwargs
) -> bytearray:
    b_array = Helpers.__to_bytelike(__o, True, *args, **kwargs)
    return b_array

def to_memoryview(__o: bytes | bytearray=None) -> memoryview:
    if isinstance(__o, (bytes, bytearray)):
        return memoryview(__o)
    invalids = (__o, [bytes, bytearray])
    raise InvalidValueError(invalids, memoryview)
