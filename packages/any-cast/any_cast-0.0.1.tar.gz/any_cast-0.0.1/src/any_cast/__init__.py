"""This module contains functions and classes whose purpose is to 
return type-casted values for both simple and complex typing 
structures.
"""
from abc import ABC, abstractmethod
from types import UnionType
from typing import (
    Any, Callable, get_args, get_origin, is_typeddict, Iterable, Mapping, Self, 
    Union
)
from binary_sequences import to_bytearray, to_bytes, to_memoryview
from booleans import to_bool
from errors import InvalidValueError, TypeCastingError
from mappings import to_dict
from numerics import to_complex, to_float, to_int
from objects import to_object
from sequences import to_list, to_range, to_tuple
from sets import to_frozenset, to_set
from text_sequences import to_str
__version__ = "0.0.1"
__all__ = [
    # Functions
    "cast",
    # Casting Containers
    "Builtins",
    "Customs",
    # Errors
    "ValueNotCastableError",
    "TargetNotSupported",
    "TargetNotCallableOrInstantiableError",
    "ValueNotCompatibleError",
    "ValueMissingEncodingError",
    "ValueTypeNotSupportedError",
    "ValueInvalidError",
    "ERRORS",
]
__refs__ = {
    "AUTHOR": {
        "Name": "Braden Toone",
        "Email": "braden@toonetown.com"
    },
    "HOMEPAGE": "https://github.com/Braden2n/StrictDataclass",
    "DOCUMENTATION": "https://github.com/Braden2n/StrictDataclass",
    "ISSUES": "https://github.com/Braden2n/StrictDataclass/issues",
    "REPOSITORY": "https://github.com",
    "CHANGELOG": "https://github.com/Braden2n/StrictDataclass/activity",
}


class TargetError(TypeCastingError):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class TargetUncallableError(TargetError):
    """Raised when the target type is not callable or instantiable."""
    def __init__(self, value: object, target_type: type) -> None:
        message = f"`{value}` is uncastable to `{target_type}`; "\
            + f"`{target_type}` is not callable or instantiable."
        super().__init__(message)


class TargetMissingCasterError(TargetError):
    """Raised when the target type does not have a caster."""
    def __init__(self, target_type: type) -> None:
        message = f"Casting to `{target_type}` target type requires a custom "\
            + f"caster. Use the `Customs.set_caster` method to set a caster."
        super().__init__(message)


class ComplexTargetNotImplementedError(TargetError, NotImplementedError):
    """Raised when a custom target type (i.e. Union, Generics) is not 
    implemented.
    """
    def __init__(self, value: object, target_type: type) -> None:
        message = f"`{value}` is uncastable to `{target_type}`; "\
            + f"`{target_type}` is a complex type that is not implemented."
        super().__init__(message)


class Caster(ABC):
    def __init__(self, value: Any, type: type, *args, **kwargs) -> None:
        self.value = value
        self.type = type
        self.kwargs = kwargs
        self.args = args
        super().__init__()
        self.__post_init__()

    @abstractmethod
    def __post_init__(self) -> None:
        ...

    @abstractmethod
    def get_caster(self, builtin: type) -> Callable[..., object]:
        ...

    @property
    @abstractmethod
    def TYPES(self) -> dict[type, tuple[Callable[..., object], object]]:
        ...


class Builtins(Caster):
    TYPES: dict[type, Callable[..., object]] = {
        bool: to_bool,
        bytearray: to_bytearray,
        bytes: to_bytes,
        complex: to_complex,
        dict: to_dict,
        float: to_float,
        frozenset: to_frozenset,
        int: to_int,
        list: to_list,
        memoryview: to_memoryview,
        range: to_range,
        set: to_set,
        str: to_str,
        tuple: to_tuple,
    }
    def __post_init__(self) -> None:
        caster = self.get_caster(self.type)
        self.casted = caster(self.value)
        
    @classmethod
    def get_caster(self, builtin: type) -> Callable[..., object]:
        return self.TYPES[builtin]

    @classmethod
    def set_caster(self, builtin: type, caster: Callable[..., object]) -> None:
        self.TYPES[builtin] = caster


class Customs(Caster):
    TYPES: dict[type, Callable[..., object]] = {
        type: to_object
    }
    def __post_init__(self) -> None:
        caster = self.get_caster(self.type)
        if isinstance(self.value, Mapping):
            self.kwargs.update(self.value)
        elif isinstance(self.value, Iterable):
            self.args = tuple(list(self.args).extend(self.value))
        elif not self.value == None:
            self.args = tuple(list(self.args).append(self.value))
        self.casted = caster(self.type, *self.args, **self.kwargs)

    @classmethod
    def get_caster(self, object: object) -> Callable[..., object]:
        if not type(object) in self.TYPES:
            raise TargetMissingCasterError(object)
        return self.TYPES[type(object)]

    @classmethod
    def set_caster(self, object: object, caster: Callable[..., object]) -> None:
        self.TYPES[type(object)] = caster

    @staticmethod
    def caster_from_value(value: Any, simple_type: type) -> Self:
        if isinstance(value, Mapping):
            caster: Caster = Customs(None, simple_type, **value)
        elif isinstance(value, Iterable):
            caster: Caster = Customs(None, simple_type, *value)
        else:
            caster: Caster = Customs(value, simple_type)
        return caster


class CastMethods:
    """Container class for casting methods """
    @staticmethod
    def to_simple(value: Any, simple_type: type) -> object:
        # Early exit for performance
        if not is_typeddict(simple_type) and isinstance(value, simple_type):
            # Catching False == 1 edge case
            if value == False and simple_type == int:
                return 1
            if value == True and simple_type == int:
                return 0
            return value
        if not callable(simple_type):
            # All targets must be callable/instantiable
            raise TargetUncallableError(value, simple_type)
        if simple_type in Builtins.TYPES:
            caster: Caster = Builtins(value, simple_type)
        else:
            caster: Caster = Customs.caster_from_value(value, simple_type)
        return caster.casted
    
    @staticmethod
    def to_union(value: Any, union_type: Union[Any, Any]) -> object:
        types = get_args(union_type)
        if isinstance(value, types):
            return value
        for target in types:
            try:
                return cast(value, target)
            except TargetError:
                # Error thrown by module (not thrown by caster)
                pass
        raise InvalidValueError(value, union_type)

    @staticmethod
    def to_complex(value: Any, complex_type: Any) -> object:
        origin = get_origin(complex_type)
        # Support for Verbose Union[T, T] and T | T
        if origin == Union or origin == UnionType:
            return CastMethods.to_union(value, complex_type)
        raise ComplexTargetNotImplementedError(value, complex_type)
            

def cast(value: object, target_type: Any) -> object:
    # Catching early exits - TypedDict cannot be called by isinstance
    if not is_typeddict(target_type) and isinstance(value, target_type):
        return value
    if get_origin(target_type) or is_typeddict(target_type):
        return CastMethods.to_complex(value, target_type)
    return CastMethods.to_simple(value, target_type)
