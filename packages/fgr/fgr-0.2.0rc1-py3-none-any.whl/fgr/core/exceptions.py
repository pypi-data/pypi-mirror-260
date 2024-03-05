__all__ = (
    'FieldAnnotationeError',
    'IncorrectCasingError',
    'IncorrectDefaultTypeError',
    'IncorrectTypeError',
    'InvalidComparisonTypeError',
    'InvalidContainerComparisonTypeError',
    'InvalidFieldRedefinitionError',
    'InvalidLogMessageTypeError',
    'MissingTypeAnnotation',
    'ReservedKeywordError',
    )

import typing

from . import constants


class Constants(constants.PackageConstants):  # noqa

    pass


class InvalidFieldRedefinitionError(KeyError):
    """Cannot add fields after a class has already been defined."""

    def __init__(self, name: str):
        self.name = name
        super().__init__(
            ' '.join(
                (
                    'Cannot add fields after a class has already',
                    'been defined.',
                    f'\nFIELD: {name}'
                    )
                )
            )


class IncorrectCasingError(SyntaxError):
    """Incorrect field casing."""

    def __init__(self, fields: typing.Iterable[str]):
        self.fields = fields
        super().__init__(
            ' '.join(
                (
                    'All fields for all Object derivatives',
                    'must be either snake_case or camelCase.'
                    f'\nFIELDS: {sorted(fields)!s}',
                    )
                )
            )

    def __reduce__(self) -> typing.Union[str, tuple[typing.Any, ...]]:
        return (
            self.__class__,
            (
                self.fields,
                )
            )


class IncorrectDefaultTypeError(SyntaxError):
    """Error raised when a field's default value is not of an allowed type."""

    def __init__(self, name: str, dtype: type[typing.Any], value: typing.Any):
        self.name = name
        self.dtype = dtype
        self.value = value
        super().__init__(
            ' '.join(
                (
                    f"Field: '{name}',",
                    f"only supports type: '{dtype!s}',",
                    f'Default supplied: {value!s}',
                    f"is of type: '{type(value)!s}'",
                    )
                )
            )

    def __reduce__(self) -> typing.Union[str, tuple[typing.Any, ...]]:
        return (
            self.__class__,
            (
                self.name,
                self.dtype,
                self.value,
                )
            )


class IncorrectTypeError(SyntaxError):
    """Error raised when a field value is not of an allowed type."""

    def __init__(
        self,
        name: str,
        dtype: typing.Union[type[typing.Any], typing._SpecialForm],
        value: typing.Any
        ):
        self.name = name
        self.dtype = dtype
        self.value = value
        super().__init__(
            ' '.join(
                (
                    f"Field: '{name}',",
                    f"only supports type: '{dtype!s}',",
                    f'Value supplied: {value!s}',
                    f"is of type: '{type(value)!s}'",
                    )
                )
            )

    def __reduce__(self) -> typing.Union[str, tuple[typing.Any, ...]]:
        return (
            self.__class__,
            (
                self.name,
                self.dtype,
                self.value,
                )
            )


class InvalidComparisonTypeError(SyntaxError):
    """Error raised when comparing a field with a value of a different type."""  # noqa

    def __init__(self, name: str, dtype: type[typing.Any], value: typing.Any):
        self.name = name
        self.dtype = dtype
        self.value = value
        super().__init__(
            ' '.join(
                (
                    f"Cannot compare field: '{name}',",
                    f"of type: '{dtype!s}',",
                    f'with the value supplied: {value!s}',
                    f"of type: '{type(value)!s}'",
                    )
                )
            )

    def __reduce__(self) -> typing.Union[str, tuple[typing.Any, ...]]:
        return (
            self.__class__,
            (
                self.name,
                self.dtype,
                self.value,
                )
            )


class InvalidContainerComparisonTypeError(SyntaxError):
    """Error raised when checking for membership or similarity against a non-Iterable field."""  # noqa

    def __init__(self, name: str, dtype: type[typing.Any], value: typing.Any):
        self.name = name
        self.dtype = dtype
        self.value = value
        super().__init__(
            ' '.join(
                (
                    f"Field: '{name}',",
                    f"of type: '{dtype!s}',",
                    f'cannot contain or be similar to: {value!s},',
                    'as this field is not an iterable.'
                    )
                )
            )

    def __reduce__(self) -> typing.Union[str, tuple[typing.Any, ...]]:
        return (
            self.__class__,
            (
                self.name,
                self.dtype,
                self.value,
                )
            )


class InvalidLogMessageTypeError(SyntaxError):
    """Error raised when a log message of invalid data type is passed."""

    def __init__(self, message: typing.Any):
        self.message = message
        super().__init__(
            ' '.join(
                (
                    'fgr can only log: `dict, str, Object` types.',
                    f"the following message of type: '{type(message)!s}' was passed.",
                    f'message: {message!s}'
                    )
                )
            )

    def __reduce__(self) -> typing.Union[str, tuple[typing.Any, ...]]:
        return (
            self.__class__,
            (
                self.message,
                )
            )


class FieldAnnotationeError(SyntaxError):
    """Incomplete type annotation."""

    def __init__(
        self,
        name: str,
        dtype: typing.Union[type[typing.Any], typing.ForwardRef]
        ):
        self.name = name
        self.dtype = dtype
        stype: str = getattr(dtype, '__name__', str(dtype))
        super().__init__(
            ' '.join(
                (
                    'All type annotations for Object derivatives',
                    'must be of a generic Field type such as',
                    '`Field[int] or Field[str]`.',
                    f'\nFIELD: {name}, TYPE: {stype}',
                    f'\nSUGGESTION: Field[{stype}]',
                    )
                )
            )

    def __reduce__(self) -> typing.Union[str, tuple[typing.Any, ...]]:
        return (
            self.__class__,
            (
                self.name,
                self.dtype
                )
            )


class MissingTypeAnnotation(SyntaxError):
    """Incomplete type annotation."""

    def __init__(self, name: str):
        self.name = name
        super().__init__(
            ' '.join(
                (
                    'Type for all Fields must be annotated.',
                    f'\nFIELD: {name}',
                    )
                )
            )


class ReservedKeywordError(SyntaxError):
    """Invalid keyword."""

    def __init__(self, name: str):
        self.name = name
        super().__init__(
            ' '.join(
                    (
                        'The following keyword is reserved for special',
                        f'purposes within {Constants.PACAKGE} and may',
                        'not be used / overwritten in class definitions.',
                        f'\nKEYWORD: {name}',
                        f'\nSUGGESTION: {name}_',
                        )
                    )
            )
