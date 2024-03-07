from typing import Iterable, Mapping
from errors import InvalidParameterError, InvalidValueError


class InvalidArgumentsError(InvalidParameterError):
    def __init__(self, args: list, target: type) -> None:
        message = f"`{args}` is not a valid list of arguments for `{target}` "\
            + f"casting"
        super().__init__(message)


class Helpers:
    @staticmethod
    def __valid_iter(__i: Iterable) -> bool:
        return all(isinstance(x, Iterable) and len(x) == 2 for x in __i)


def to_dict(*args, **kwargs) -> dict:
    if len(args) == 0:
        return dict(**kwargs)
    if len(args) > 1:
        raise InvalidArgumentsError(args, dict)
    iter_map = args[0]
    if isinstance(iter_map, Mapping):
        return dict(iter_map, **kwargs)
    if isinstance(iter_map, Iterable) and Helpers.__valid_iter(iter_map):
        print("I'm a valid iterable")
        return dict(iter_map, **kwargs)
    invalids = (iter_map, [Iterable, Mapping])
    raise InvalidValueError(invalids, dict)
