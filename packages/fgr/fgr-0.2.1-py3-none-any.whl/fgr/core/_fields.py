__all__ = (
    'Field',
    )

import json
import typing

from . import constants
from . import dtypes
from . import utils

if typing.TYPE_CHECKING:
    from . import fields


class Constants(constants.PackageConstants):  # noqa

    pass


class Field(dict, typing.Generic[dtypes.GenericType]):
    """
    Placeholder till public definition of `fields.Field` is available \
    to the program.

    ---

    Retains primary `fields.Field` access functionality, but lacks \
    `query.Query` construction logic.

    """

    name: str
    type: typing.Type[dtypes.GenericType]
    default: dtypes.GenericType
    nullable: bool
    required: bool
    enum: dtypes.Enum

    @typing.overload
    def __get__(
        self,
        object_: None,
        dtype: typing.Type['fields.Field']
        ) -> 'Field[dtypes.GenericType]': ...
    @typing.overload
    def __get__(
        self,
        object_: 'fields.Field',
        dtype: typing.Type['fields.Field']
        ) -> dtypes.GenericType: ...
    def __get__(
        self,
        object_: typing.Optional['fields.Field'],
        dtype: typing.Type['fields.Field']
        ) -> typing.Union['Field[dtypes.GenericType]', dtypes.GenericType]:
        if object_ is None:
            field: 'Field[dtypes.GenericType]' = dtype[self['name']]
            return field
        else:
            value: dtypes.GenericType = object_[self['name']]
            return value

    def __getattribute__(self, __name: str) -> typing.Any:
        if __name in self:
            return self[__name]
        else:
            return super().__getattribute__(__name)

    def __field_hash__(self) -> int:
        return hash(
            ''.join(
                (
                    self.__class__.__name__,
                    repr(self.type) or str(),
                    repr(self.default) or str(),
                    self.name or str()
                    )
                )
            )

    def __repr__(self) -> str:
        """Return field represented as a neatly formatted JSON string."""

        return json.dumps(
            dict(self),
            default=utils.convert_for_representation,
            indent=Constants.INDENT,
            sort_keys=True
            )

    def __init__(
        self,
        /,
        *,
        name: str = None,
        type: typing.Optional[typing.Type[dtypes.GenericType]] = None,
        default: typing.Any = None,
        nullable: bool = True,
        required: bool = False,
        enum: dtypes.Enum = None,
        **kwargs: typing.Any
        ):
        return super().__init__(
            name=name,
            type=type,
            default=default,
            nullable=nullable,
            required=required,
            enum=enum,
            **kwargs
            )
