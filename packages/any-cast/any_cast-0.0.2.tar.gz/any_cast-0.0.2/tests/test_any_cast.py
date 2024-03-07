import os
os.chdir(os.path.dirname(__file__))
from sys import path
path.append('../src')
for p in path:
    print(p)
# path.append(__file__)
# from os.path import join, dirname
# from sys import path
# path.append(join())
# path.append("../src")
from src.any_cast import cast, ERRORS, Builtins, Defaults
from unittest import TestCase



class TestBuiltins(TestCase):
    @classmethod
    def assert_all_casts_fail(cls, objs: list[object], type: type) -> None:
        for obj in objs:
            cls.assert_fails(obj, type)

    @classmethod
    def assert_all_casts_pass(cls, objs: list[object], type: type) -> None:
        for obj in objs:
            cls.assert_passes(obj, type)

    def assert_fails(self, obj: object, type: type) -> None:
        with self.assertRaises(ERRORS):
            cast(obj, type)

    def assert_passes(self, obj: object, type: type) -> None:
        try:
            cast(obj, type)
        except ERRORS as e:
            self.fail(f"Failed with {type(e)}")

    def test_bool(self) -> None:
        _type = bool
        for _, (_, instance) in Builtins.TYPES.items():
            if type(instance) in []:
                self.cast_should_raise(instance, _type)
            else: 
                self.cast_should_not_raise(instance, _type)

    def test_bytearray(self) -> None:
        _type = bytearray
        for _, (_, instance) in Builtins.TYPES.items():
            if type(instance) in [int, float, complex, bool, str]:
                self.cast_should_raise(instance, _type)
            else: 
                self.cast_should_not_raise(instance, _type)

    def test_bytes(self) -> None:
        _type = bytearray
        for _, (_, instance) in Builtins.TYPES.items():
            if type(instance) in [int, float, complex, bool, str]:
                self.cast_should_raise(instance, _type)
            else: 
                self.cast_should_not_raise(instance, _type)

    def test_complex(self) -> None:
        _type = complex
        for _, (_, instance) in Builtins.TYPES.items():
            if not type(instance) in []:
                self.cast_should_raise(instance, _type)
            else: 
                self.cast_should_not_raise(instance, _type)

    def test_dict(self) -> None:
        _type = dict
        for _, (_, instance) in Builtins.TYPES.items():
            if not type(instance) in [dict]:
                self.cast_should_raise(instance, _type)
            else: 
                self.cast_should_not_raise(instance, _type)

    def test_float(self) -> None:
        _type = float
        for _, (_, instance) in Builtins.TYPES.items():
            if type(instance) in [complex]:
                self.cast_should_raise(instance, _type)
            else: 
                self.cast_should_not_raise(instance, _type)

    def test_frozenset(self) -> None:
        _type = frozenset
        for _, (_, instance) in Builtins.TYPES.items():
            if type(instance) in [int, float, complex, bool]:
                self.cast_should_raise(instance, _type)
            else: 
                self.cast_should_not_raise(instance, _type)

    def test_int(self) -> None:
        _type = int
        for _, (_, instance) in Builtins.TYPES.items():
            if type(instance) in [complex]:
                self.cast_should_raise(instance, _type)
            else: 
                self.cast_should_not_raise(instance, _type)

    def test_list(self) -> None:
        _type = list
        for _, (_, instance) in Builtins.TYPES.items():
            if type(instance) in [int, float, complex, bool]:
                self.cast_should_raise(instance, _type)
            else: 
                self.cast_should_not_raise(instance, _type)

    def test_memoryview(self) -> None:
        _type = memoryview
        for _, (_, instance) in Builtins.TYPES.items():
            if not type(instance) in [memoryview]:
                self.cast_should_raise(instance, _type)
            else: 
                self.cast_should_not_raise(instance, _type)

    def test_range(self) -> None:
        _type = range
        for _, (_, instance) in Builtins.TYPES.items():
            if not type(instance) in [memoryview]:
                self.cast_should_raise(instance, _type)
            else: 
                self.cast_should_not_raise(instance, _type)

    def test_set(self) -> None:
        _type = set
        for _, (_, instance) in Builtins.TYPES.items():
            if type(instance) in []:
                self.cast_should_raise(instance, _type)
            else: 
                self.cast_should_not_raise(instance, _type)

    def test_str(self) -> None:
        _type = str
        for _, (_, instance) in Builtins.TYPES.items():
            if type(instance) in []:
                self.cast_should_raise(instance, _type)
            else: 
                self.cast_should_not_raise(instance, _type)

    def test_tuple(self) -> None:
        _type = tuple
        for _, (_, instance) in Builtins.TYPES.items():
            if type(instance) in []:
                self.cast_should_raise(instance, _type)
            else: 
                self.cast_should_not_raise(instance, _type)
