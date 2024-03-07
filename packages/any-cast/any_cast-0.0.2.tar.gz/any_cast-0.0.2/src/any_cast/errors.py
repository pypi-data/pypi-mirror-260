from typing import Iterable


class TypeCastingError(TypeError):
    def __init__(self, message: str) -> None:
        super().__init__(f"\n\tCasting Failed:\n\t{message}")


class InvalidParameterError(TypeCastingError):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class InvalidEncodingError(InvalidParameterError):
    def __init__(self, encoding: object, target: type, err: bool=False) -> None:
        if err:
            message = f"`{encoding}` is not a valid encoding for `{target}` "\
                + f"casting"
        else:
            message = f"`{encoding}` must be a `str` (not `{type(encoding)}`) "\
                + f"to be used as a valid encoding for `{target}` casting"
        super().__init__(message)


class InvalidErrorsError(InvalidParameterError):
    def __init__(self, errors: object, target: type, err: bool=False) -> None:
        if err:
            message = f"`{errors}` is not a valid errors for `{target}` "\
                + f"casting"
        else:
            message = f"`{errors}` must be a `str` (not `{type(errors)}`) to "\
                + f"be used as a valid errors status for `{target}` casting"
        super().__init__(message)


class ValueCastingError(ValueError):
    def __init__(self, message: str) -> None:
        super().__init__(f"\n\t{message}")


class InvalidValueError(ValueCastingError):
    def __init__(
        self, 
        values: list[tuple[object, type]] | tuple[object, list[type]] | object, 
        target: type
    ) -> None:
        if isinstance(values, list):
            message = "".join([f"\n\t`{v[0]}` of type `{type(v[0])}` was "\
                + f"{f'valid' if isinstance(v[0], v[1]) else f'invalid as {v[1]}'}"\
                + f" in `{target}` cast" for v in values]
            ).lstrip("\n\t")
        elif isinstance(values, tuple):
            message = f"`{values[0]}` is not a "\
                + f"{self.oxford_join(values[1], ', ', ', or')}"
        else:
            message += f"`{values}` of type `{values}` is uncastable to "\
                + f"`{target}` as attempted"
        super().__init__(message)

    @staticmethod
    def oxford_join(
        i: Iterable, delim: str=', ', last_delim: str=', and'
    ) -> str:
        joined = delim.join(i)
        index = joined.rfind(delim)
        if index != 1:
            joined = joined[:index] + last_delim + joined[index + len(delim):]
        return joined
