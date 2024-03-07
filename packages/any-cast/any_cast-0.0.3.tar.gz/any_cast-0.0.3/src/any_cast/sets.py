from typing import Iterable
from .errors import InvalidValueError


def to_set(__i: Iterable):
    if isinstance(__i, Iterable):
        return set(__i)
    raise InvalidValueError((__i, [Iterable]), set)

@staticmethod
def to_frozenset(__i: Iterable):
    if isinstance(__i, Iterable):
        return frozenset(__i)
    raise InvalidValueError((__i, [Iterable]), frozenset)
