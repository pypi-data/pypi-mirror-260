from typing import Any
from errors import (
    InvalidParameterError, InvalidValueError, TypeCastingError, 
    ValueCastingError
)


class BaseNotAllowedError(TypeCastingError):
    def __init__(self, base: object) -> None:
        message = f"Explicit base `{base}` is not allowed when casting to an "\
            + f"`int` from a real number"
        super().__init__(message)


class InvalidBaseError(InvalidParameterError):
    def __init__(self, base: object) -> None:
        message = f"`{base}` is not a valid integer base for `int` casting"
        super().__init__(message)


class LimitExceededError(ValueCastingError):
    def __init__(self, value: object, base: int) -> None:
        base_msg = " (not power-of-2)" if self.is_pow_of_two(base) else ""
        message = f"Potential DOS threat: `{value}` is uncastable to base"\
            + f"`{base}`{base_msg} integer - non-linear castings must be manual"
        super().__init__(message)

    @staticmethod
    def is_pow_of_two(n: int) -> bool:
        # Bitwise AND to check only first bit is 1
        # Valid powers of two have *only* the first bit set to 1
        # Predecessor (n - 1) should have all bits set to 1
        # n & (n - 1) completes bitwise operation
        # Operation is always 0 in valid cases
        return n != 0 and (n & (n - 1)) == 0
    

class FloatPrecisionExceededError(ValueCastingError):
    def __init__(self, value: object) -> None:
        message = f"Python precision exceeded when casting `{value}` to `float`"
        super().__init__(message)


class ValueMalformattedError(ValueCastingError):
    def __init__(self, value: object, target: type) -> None:
        message = f"`{value}` is malformatted for cast to `{target}`"
        super().__init__(message)


class Real:
    def __instancecheck__(self, __instance: Any) -> bool:
        if isinstance(__instance, (int, float)):
            return True
        return False


class Numeric:
    def __instancecheck__(self, __instance: Any) -> bool:
        if isinstance(__instance, (Real, complex)):
            return True
        return False


class ValidBase:
    def __instancecheck__(self, __instance: Any) -> bool:
        # Must be an integer greater than 0 according to spec
        if isinstance(__instance, int) and __instance > 0:
            return True
        return False
    

class BufferReadable:
    def __instancecheck__(self, __instance: Any) -> bool:
        if isinstance(__instance, (str, bytes, bytearray)):
            return True
        return False


class Helpers:
    @staticmethod
    def __real_to_int(__x: Real=0) -> int:
        return int(__x)

    @staticmethod
    def __str_to_int(__x: BufferReadable, base: int=10) -> int:
        return int(__x, base=base)

    @staticmethod
    def __str_to_complex(string: str) -> complex:
        return complex(string)

    @staticmethod
    def __numeric_to_complex(real: Numeric, imag: Numeric) -> complex:
        return complex(real, imag)


def to_int(__x: Real | BufferReadable=None, base: ValidBase=None) -> int:
    if __x is None:
        return 0
    if isinstance(__x, Real):
        # Real numbers cannot be passed with explicit base
        if not base is None:
            raise BaseNotAllowedError(base)
        return Helpers.__real_to_int(__x)
    if not isinstance(__x, BufferReadable):
        raise InvalidValueError(__x, int)
    if not isinstance(base, ValidBase):
        raise InvalidBaseError(base)
    try:
        return Helpers.__str_to_int(__x, base=base)
    except ValueError:
        # Captures Python DOS prevention limit error
        raise LimitExceededError(__x, base)
    
@staticmethod
def to_float(__x: Real | str=None, /) -> float:
    if __x is None:
        return 0.0
    if not isinstance(__x, (Real, str)):
        raise InvalidValueError(__x, float)
    try:
        float(__x)
    except OverflowError:
        # Captures float range exceeded overflows
        raise FloatPrecisionExceededError(__x)
    except ValueError:
        # Captures all invalid formatting errors
        raise ValueMalformattedError(__x)

def to_complex(num_or_str: Numeric | str=None, imag: Numeric=0) -> complex:
    if num_or_str is None:
        return 0j
    if isinstance(num_or_str, str):
        try:
            return Helpers.__str_to_complex(num_or_str)
        except ValueError:
            raise ValueMalformattedError(num_or_str)
    if not isinstance(num_or_str, Numeric) or not isinstance(imag, Numeric):
        invalids = [(num_or_str, Numeric), (imag, Numeric)]
        raise InvalidValueError(invalids, complex)
    return Helpers.__numeric_to_complex(num_or_str, imag)
