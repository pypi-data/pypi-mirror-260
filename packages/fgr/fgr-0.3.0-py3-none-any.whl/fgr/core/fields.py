__all__ = (
    'Field',
    )

import json
import typing

from . import _fields

from . import constants
from . import dtypes
from . import enums
from . import exceptions
from . import meta
from . import modules
from . import utils

if typing.TYPE_CHECKING:
    from . import query


class Constants(constants.PackageConstants):  # noqa

    pass


@dtypes.dataclass_transform(
    eq_default=True,
    kw_only_default=True,
    field_specifiers=(_fields.Field, ),
    )
class Field(  # type: ignore[misc]
    meta.Base,
    typing.Generic[dtypes.GenericType],
    ):
    """
    Simple field object.

    ---

    ### Querying

    Queries for `Objects` can be generated from their fields \
    using the following comparison operators:

    * `field_1_eq_filter = Object.field_1 == 'test_value_123'`
    * `field_1_ne_filter = Object.field_1 != 'test_value_123'`
    * `field_1_ge_filter = Object.field_1 >= 'test_value_123'`
    * `field_1_gt_filter = Object.field_1 > 'test_value_123'`
    * `field_1_le_filter = Object.field_1 <= 'test_value_123'`
    * `field_1_lt_filter = Object.field_1 < 'test_value_123'`

    And the following special operators:

    * `field_1_contains_filter = Object.field_1 << 'test_value_123'`
    * `field_1_similarity_filter = Object.field_1 % 'test_value_123'`
    * `field_1_similarity_filter_with_threshold = Object.field_1 % ('test_value_123', 0.8)`

    Queries may be chained together using the `&` and `|` bitwise \
    operators, corresponding to `and` and `or` clauses respectively.

    Additionally, the invert (`~`) operator may be prefixed to any \
    Query to match the opposite of any conditions specified \
    instead.

    ---

    ### Example

    ```py
    query: Query = (
        (
            (Object.integer_field >= 1)
            | (Object.string_field % ('test', 0.75))
            )
        & ~(Object.list_field << 'test')
        )
    ```

    In the example above, the query would match any `Object` for which \
    the string `'test'` is `not` a member of `list_field` and for which \
    either the value for `integer_field` is greater than or equal to `1` \
    or the value for `string_field` is at least `75%` similar to `'test'`.

    """

    if typing.TYPE_CHECKING:
        __fields__: typing.ClassVar[typing.Mapping[str, _fields.Field]] = {}

    name: _fields.Field[str] = None
    type: _fields.Field[typing.Type[dtypes.GenericType]] = None
    default: _fields.Field[dtypes.GenericType] = None
    nullable: _fields.Field[bool] = True  # type: ignore[assignment]
    required: _fields.Field[bool] = False  # type: ignore[assignment]
    enum: _fields.Field[dtypes.Enum] = None

    @typing.overload
    def __get__(
        self,
        object_: None,
        dtype: dtypes.MetaType
        ) -> 'Field[dtypes.GenericType]': ...
    @typing.overload
    def __get__(
        self,
        object_: 'meta.Base',
        dtype: dtypes.MetaType
        ) -> dtypes.GenericType: ...
    def __get__(
        self,
        object_: typing.Optional['meta.Base'],
        dtype: dtypes.MetaType
        ) -> typing.Union['Field[dtypes.GenericType]', dtypes.GenericType]:  # pragma: no cover
        pass

    def __repr__(self) -> str:
        """Return object represented as a neatly formatted JSON string."""

        return json.dumps(
            dict(self),
            default=utils.convert_for_representation,
            indent=Constants.INDENT,
            sort_keys=True
            )

    def __init__(
        self,
        /,
        default: typing.Any = None,
        nullable: bool = True,
        required: bool = False,
        enum: dtypes.Enum = None,
        type: typing.Type[dtypes.GenericType] = None,
        **kwargs: typing.Any
        ):
        self.name = kwargs.get('name')
        self.type = type
        self.default = default
        self.nullable = nullable
        self.required = required
        self.enum = enum
        self.__post_init__()

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

    @typing.overload  # type: ignore[override]
    def __lshift__(self, value: dtypes.FieldType) -> dtypes.FieldType: ...  # type: ignore[overload-overlap]
    @typing.overload
    def __lshift__(
        self,
        value: typing.Any
        ) -> 'query.ContainsQueryCondition': ...
    def __lshift__(
        self,
        value: typing.Any
        ) -> typing.Union['query.ContainsQueryCondition', dtypes.FieldType]:
        if utils.is_field_type(value):
            return super().__lshift__(value)  # type: ignore[operator]
        self._validate_container_comparison(value)
        q: 'query.ContainsQueryCondition' = (
            modules.Modules().query.ContainsQueryCondition(  # type: ignore[attr-defined]
                field=self.name,
                contains=value
                )
            )
        return q

    @typing.overload  # type: ignore[override]
    def __eq__(self, value: dtypes.FieldType) -> bool: ...  # type: ignore[overload-overlap]
    @typing.overload
    def __eq__(
        self,
        value: typing.Any
        ) -> 'query.EqQueryCondition': ...
    def __eq__(
        self,
        value: typing.Any
        ) -> typing.Union['query.EqQueryCondition', bool]:
        if utils.is_field_type(value):
            return self.__field_hash__() == value.__field_hash__()
        self._validate_comparison(value)
        q: 'query.EqQueryCondition' = (
            modules.Modules().query.EqQueryCondition(  # type: ignore[attr-defined]
                field=self.name,
                eq=value
                )
            )
        return q

    @typing.overload  # type: ignore[override]
    def __ne__(self, value: dtypes.FieldType) -> bool: ...  # type: ignore[overload-overlap]
    @typing.overload
    def __ne__(
        self,
        value: typing.Any
        ) -> 'query.NeQueryCondition': ...
    def __ne__(
        self,
        value: typing.Any
        ) -> typing.Union['query.NeQueryCondition', bool]:
        if utils.is_field_type(value):
            return self.__field_hash__() != value.__field_hash__()
        self._validate_comparison(value)
        q: 'query.NeQueryCondition' = (
            modules.Modules().query.NeQueryCondition(  # type: ignore[attr-defined]
                field=self.name,
                ne=value
                )
            )
        return q

    def __mod__(
        self,
        value: typing.Union[tuple[typing.Any, float], typing.Any]
        ) -> 'query.SimilarQueryCondition':
        if isinstance(value, tuple):
            value, threshold = value
        else:
            threshold = enums.MatchThreshold.default.value
        self._validate_container_comparison(value)
        self._validate_comparison(value)
        q: 'query.SimilarQueryCondition' = (
            modules.Modules().query.SimilarQueryCondition(  # type: ignore[attr-defined]
                field=self.name,
                like=value,
                threshold=threshold
                )
            )
        return q

    def __gt__(self, value: dtypes.GenericType) -> 'query.GtQueryCondition':
        self._validate_comparison(value)
        q: 'query.GtQueryCondition' = (
            modules.Modules().query.GtQueryCondition(  # type: ignore[attr-defined]
                field=self.name,
                gt=value
                )
            )
        return q

    def __ge__(self, value: dtypes.GenericType) -> 'query.GeQueryCondition':
        self._validate_comparison(value)
        q: 'query.GeQueryCondition' = (
            modules.Modules().query.GeQueryCondition(  # type: ignore[attr-defined]
                field=self.name,
                ge=value
                )
            )
        return q

    def __lt__(self, value: dtypes.GenericType) -> 'query.LtQueryCondition':
        self._validate_comparison(value)
        q: 'query.LtQueryCondition' = (
            modules.Modules().query.LtQueryCondition(  # type: ignore[attr-defined]
                field=self.name,
                lt=value
                )
            )
        return q

    def __le__(self, value: dtypes.GenericType) -> 'query.LeQueryCondition':
        self._validate_comparison(value)
        q: 'query.LeQueryCondition' = (
            modules.Modules().query.LeQueryCondition(  # type: ignore[attr-defined]
                field=self.name,
                le=value
                )
            )
        return q

    def _validate_comparison(self, value: typing.Any) -> None:
        if (
            self.type
            and 'Union' in self.type.__class__.__name__
            and type(value) not in typing.get_args(self.type)
            ):
            raise exceptions.InvalidComparisonTypeError(
                self.name,
                self.type,
                value
                )
        elif not isinstance(
            value,
            (
                *getattr(self.type, '__args__', (self.type, )),
                dtypes.NoneType,
                )
            ):
            raise exceptions.InvalidComparisonTypeError(
                self.name,
                self.type,
                value
                )

    def _validate_container_comparison(self, value: typing.Any) -> None:
        if not issubclass(self.type, typing.Iterable):
            raise exceptions.InvalidContainerComparisonTypeError(
                self.name,
                self.type,
                value
                )

    def parse_dtype(
        self,
        v: typing.Union[typing.Any, str],
        t: typing.Type[typing.Any] = None,
        validate_dtype: bool = True,
        ) -> typing.Any:
        """
        Return correctly typed value if possible, None otherwise, or \
        (optionally) raise an error if an invalid value is passed.

        """

        if v is None and not self.nullable and validate_dtype:
            raise exceptions.IncorrectTypeError(self.name, self.type, v)
        elif v is None:
            return v
        elif 'Union' in (t := (t or self.type)).__name__:
            for _t in typing.get_args(t):
                if (parsed := self.parse_dtype(v, _t, validate_dtype=False)):
                    return parsed
            else:
                if validate_dtype:
                    raise exceptions.IncorrectTypeError(
                        self.name,
                        self.type,
                        v
                        )
        elif isinstance(v, str) and not issubclass(t, str):
            if issubclass(
                typing.get_origin(t) or t,
                (meta.Base, *typing.get_args(dtypes.Container))
                ):
                return self.parse_dtype(
                    json.loads(v),
                    t,
                    validate_dtype=validate_dtype
                    )
            elif issubclass(t, bool) and v.lower() in {'true', 'false'}:
                return bool(v.title())
            elif issubclass(t, typing.get_args(dtypes.NumberType)) and (
                (p := v.partition('.'))[0].isnumeric()
                or (p[1] and p[2].isnumeric())
                ):
                return t(v)
            elif v.lower() in {'null', 'none'}:
                return self.parse_dtype(
                    None,
                    t,
                    validate_dtype=validate_dtype
                    )
            elif validate_dtype:
                raise exceptions.IncorrectTypeError(self.name, self.type, v)
        elif isinstance(v, dict) and issubclass(t, meta.Base):
            return t(v)
        elif (
            isinstance(v, typing.Iterable)
            and issubclass(
                (o := typing.get_origin(t) or t),
                typing.get_args(dtypes.Container)
                )
            ):
            if not (generics := getattr(t, '__args__', ())):
                return o(v)
            elif isinstance(v, typing.Mapping):
                return o(
                    **{
                        self.parse_dtype(
                            k,
                            generics[0],
                            validate_dtype=validate_dtype
                            ): (
                                self.parse_dtype(
                                    _v,
                                    generics[1],
                                    validate_dtype=validate_dtype
                                    )
                                )
                        for k, _v
                        in v.items()
                        }
                    )
            else:
                return o(
                    self.parse_dtype(
                        k,
                        generics[0],
                        validate_dtype=validate_dtype
                        )
                    for k
                    in v
                    )
        elif isinstance(v, typing.get_origin(t) or t):
            return v
        elif validate_dtype:
            raise exceptions.IncorrectTypeError(self.name, self.type, v)

        return None
