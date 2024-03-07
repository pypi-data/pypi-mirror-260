from typing import Iterable
from .errors import InvalidValueError


def to_list(__i: Iterable=None) -> list:
    if __i is None:
        return []
    if not isinstance(__i, Iterable):
        raise InvalidValueError(__i, list)
    return list(__i)

def to_tuple(__i: Iterable=None) -> tuple:
    if __i is None:
        return ()
    if not isinstance(__i, Iterable):
        raise InvalidValueError(__i, tuple)
    return tuple(__i)

def to_range(__start_stop: int, __stop: int=None, __step: int=1) -> range:
    if __stop is None:
        return range(__start_stop)
    if (
        not isinstance(__start_stop, int)
        or not isinstance(__stop, int) 
        or not isinstance(__step, int)
    ):
        invalids = [(__start_stop, int), (__stop, int), (__step, int)]
        raise InvalidValueError(invalids, range)
    return range(__start_stop, __stop, __step)
