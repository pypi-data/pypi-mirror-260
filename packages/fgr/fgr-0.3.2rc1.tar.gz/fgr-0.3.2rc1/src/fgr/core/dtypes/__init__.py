__all__ = (
    'dataclass_transform',
    'Array',
    'BaseType',
    'Default',
    'Enum',
    'Field',
    'FieldType',
    'GenericType',
    'Immutable',
    'MetaType',
    'NoneType',
    'NumberType',
    'Primitive',
    'RePatternDict',
    'Query',
    'QueryType',
    'Serial',
    'SupportsFields',
    'Type',
    'ValidLogType',
    )

import collections
import decimal
import enum
import re
import sys
import types
import typing

if typing.TYPE_CHECKING:
    from .. import _fields
    from .. import fields
    from .. import meta
    from .. import query

from . import constants
from . import utils


class Constants(constants.TypeConstants):  # noqa

    pass


T = typing.TypeVar('T')
Default = typing.TypeVar('Default')
Type = typing.TypeVar('Type', bound=type[typing.Any])
BaseType = typing.TypeVar('BaseType', bound='meta.Base')
GenericType = typing.TypeVar('GenericType', bound=typing.Any)
MetaType = typing.TypeVar('MetaType', bound='meta.Meta')

Array = typing.Union[
    collections.deque,
    frozenset,
    list,
    set,
    tuple,
    ]
Enum = typing.Union[
    enum.EnumMeta,
    Array
    ]
Container = typing.Union[
    Array,
    collections.OrderedDict,
    collections.defaultdict,
    dict,
    ]
FieldType = typing.Union[
    '_fields.Field',
    'fields.Field'
    ]
NoneType = None.__class__
NumberType = typing.Union[
    decimal.Decimal,
    float,
    int,
    ]
Primitive = typing.Union[
    bool,
    bytes,
    float,
    int,
    str,
    ]
Serial = typing.Union[
    Primitive,
    dict,
    list
    ]
Immutable = typing.Union[
    Primitive,
    enum.EnumMeta,
    frozenset,
    tuple,
    ]
Query = typing.Union[
    'query.Query',
    'query.QueryCondition',
    'query.AndQuery',
    'query.OrQuery',
    'query.InvertQuery',
    'query.ContainsQueryCondition',
    'query.EqQueryCondition',
    'query.NeQueryCondition',
    'query.LeQueryCondition',
    'query.LtQueryCondition',
    'query.GeQueryCondition',
    'query.GtQueryCondition',
    ]
QueryType = typing.TypeVar('QueryType', bound=Query)
ValidLogType = typing.Union[
    str,
    dict,
    'meta.Base',
    'meta.Meta'
    ]


class SupportsFields(typing.Protocol):
    """Meta protocol."""

    if typing.TYPE_CHECKING:
        __fields__: typing.ClassVar[typing.Mapping[str, FieldType]] = {}
        __heritage__: typing.ClassVar[tuple[type['meta.Base'], ...]] = ()
        __cache__: typing.ClassVar[dict[str, typing.Any]] = {}

        description: typing.ClassVar[str] = Constants.UNDEFINED
        distribution: typing.ClassVar[str] = Constants.UNDEFINED
        enumerations: typing.ClassVar[dict[str, list]] = {}
        fields: typing.ClassVar[tuple[str, ...]] = ()
        hash_fields: typing.ClassVar[tuple[str, ...]] = ()
        reference: typing.ClassVar[str] = Constants.UNDEFINED
        is_snake_case: typing.ClassVar[bool] = True
        isCamelCase: typing.ClassVar[bool] = False


class Field(types.GenericAlias):
    """Generic alias type."""

    def __repr__(self) -> str:
        ftypes = typing.get_args(self)
        _delim = (
            ' | '
            if isinstance(self, typing._UnionGenericAlias)  # type: ignore[attr-defined]
            else ', '
            )
        _ftypes = _delim.join(
            (
                getattr(t, '__name__', 'Any')
                for t
                in ftypes
                )
            )
        return f'Field[{_ftypes}]'


class RePatternDict(typing.TypedDict):

    ID: str
    Severity: str
    Title: str
    Regex: re.Pattern


if sys.version_info < (3, 11):  # pragma: no cover

    P = typing.ParamSpec('P')
    R = typing.TypeVar('R')

    def dataclass_transform(
        *,
        eq_default: bool = True,
        order_default: bool = False,
        kw_only_default: bool = False,
        frozen_default: bool = False,
        field_specifiers: tuple[type[typing.Any] | typing.Callable[..., typing.Any], ...] = (),  # noqa
        **kwargs: typing.Any,
        ) -> R:  # type: ignore[type-var]
        def outer(data_class: typing.Callable[P, R]) -> R:
            data_class.__dataclass_transform__ = {  # type: ignore[attr-defined]
                "eq_default": eq_default,
                "order_default": order_default,
                "kw_only_default": kw_only_default,
                "frozen_default": frozen_default,
                "field_specifiers": field_specifiers,
                "kwargs": kwargs,
                }
            def inner(*args: P.args, **kwargs: P.kwargs) -> R:
                return data_class(*args, **kwargs)
            return data_class  # type: ignore[return-value]
        return outer  # type: ignore[return-value]

else:  # pragma: no cover

    from typing import dataclass_transform
