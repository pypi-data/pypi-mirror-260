from .errors import InvalidEncodingError, InvalidErrorsError, InvalidValueError


class Helpers:
    @staticmethod
    def __params_to_str(
        __o: bytes | bytearray, encoding: str='utf-8', errors: str='strict'
    ) -> str:
        return str(__o, encoding, errors)

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


def to_str(__o: bytes | bytearray | object=None, *args, **kwargs) -> str:
    if __o is None:
        return ''
    if len(args) > 0 or len(kwargs) > 0:
        if not isinstance(__o, (bytes, bytearray)):
            invalids = (__o, [bytes, bytearray])
            raise InvalidValueError(invalids, str)
        encoding, errors = Helpers.__get_params(*args, **kwargs)
        if not isinstance(encoding, str):
            raise InvalidEncodingError(errors, str)
        if not isinstance(errors, str):
            raise InvalidErrorsError(errors, str)
        try:
            return Helpers.__params_to_str(__o, encoding, errors)
        except (RuntimeError, MemoryError):
            raise InvalidValueError(__o, str)
        except LookupError:
            raise InvalidEncodingError(encoding, str, True)
    try:
        return str(__o)
    except (RuntimeError, MemoryError):
        raise InvalidValueError(__o, str)
