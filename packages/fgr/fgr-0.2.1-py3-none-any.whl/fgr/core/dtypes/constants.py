import typing

from .. import constants


class TypeConstants(constants.PackageConstants):
    """Constants for dtypes."""

    NONE_TYPES: tuple[typing.Any, typing.Any, typing.Any] = (
        None,
        None.__class__,
        typing.Literal[None]
        )
