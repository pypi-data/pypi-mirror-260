__all__ = (
    'Base',
    'Meta',
    )

import copy
import json
import typing
import sys

from . import constants
from . import dtypes
from . import exceptions
from . import modules
from . import utils

if typing.TYPE_CHECKING:
    from . import _fields
    from . import fields as fields_


class Constants(constants.PackageConstants):  # noqa

        pass


class Meta(type):
    """Base class constructor."""

    if typing.TYPE_CHECKING:
        __fields__: typing.ClassVar[typing.Mapping[str, dtypes.FieldType]] = {}
        __heritage__: typing.ClassVar[tuple[type['Base'], ...]] = ()
        __cache__: typing.ClassVar[dict[str, typing.Any]] = {}

        description: typing.ClassVar[str] = Constants.UNDEFINED
        distribution: typing.ClassVar[str] = Constants.UNDEFINED
        enumerations: typing.ClassVar[dict[str, list]] = {}
        fields: typing.ClassVar[tuple[str, ...]] = ()
        hash_fields: typing.ClassVar[tuple[str, ...]] = ()
        reference: typing.ClassVar[str] = Constants.UNDEFINED
        is_snake_case: typing.ClassVar[bool] = True
        isCamelCase: typing.ClassVar[bool] = False

    def __new__(
        mcs: type[dtypes.MetaType],
        __name: str,
        __bases: tuple[type, ...],
        __namespace: dict[str, typing.Any],
        **kwargs: typing.Any
        ) -> dtypes.MetaType:
        fields: dict[str, dtypes.FieldType] = {}
        heritage: tuple[type, ...] = __bases
        slots: list[str] = (
            [_slots,]
            if isinstance(
                (
                    _slots := __namespace.get(
                        '__slots__',
                        ()
                        )
                    ),
                str
                )
            else list(_slots)
            )

        module = __namespace.get('__module__', '')
        annotations = dtypes.utils.resolve_annotations(
            __namespace.pop('__annotations__', {}),
            sys.modules[module].__dict__
            )

        base_count = 0
        for _base in reversed(__bases):
            if isinstance(_base, Meta):
                base_count += 1
                fields.update(_base.__fields__)

        if base_count > 1:
            common_annotations: dict[str, type[typing.Any]] = {}
            common_base_names: list[str] = []
            common_bases: list[type['Base']] = []
            common_namespace: dict[str, typing.Any] = {}
            common_slots: list[str] = []
            for _base in reversed(__bases):
                for __base in reversed(_base.__mro__):
                    if issubclass(__base, Base) and __base is not Base:
                        if __base.__name__ not in common_base_names:
                            common_base_names.insert(0, __base.__name__)
                            common_bases.insert(0, __base)
                            common_namespace.update(__base.__dict__)
                            for slot in __base.__slots__:
                                if slot not in common_slots:
                                    common_slots.append(slot)
                            common_annotations.update(__base.__annotations__)
            common_namespace = {
                k: v
                for k, v
                in common_namespace.items()
                if (
                    utils.is_valid_keyword(k)
                    and k not in common_slots
                    )
                }
            common_namespace['__annotations__'] = common_annotations
            common_namespace['__slots__'] = tuple(common_slots)
            common_base = Meta(
                Constants.DELIM_REBASE.join(common_base_names[:base_count]),
                (Base, ),
                common_namespace
                )
            __bases = (common_base, )

        if module != Constants.META_MODULE:
            base_fields = set(fields.keys())
            defaults: list[str] = []
            for name, default in __namespace.items():
                if (
                    not utils.is_valid_keyword(name)
                    and module != Constants.FIELDS_MODULE
                    ):
                    raise exceptions.ReservedKeywordError(name)
                elif (
                    default.__class__.__name__ == 'Field'
                    or (
                        isinstance(default, dict)
                        and default
                        and (
                            is_field_as_dict := all(
                                k in Constants.FIELD_KEYS
                                for k
                                in default
                                ) and module != Constants.FIELDS_MODULE
                            )
                        )
                    ):
                    if (
                        isinstance(default, dict)
                        and default
                        and is_field_as_dict
                        ):
                        default = modules.Modules().fields.Field(  # type: ignore[attr-defined]
                            **__namespace.get(name)
                            )
                    else:
                        default = __namespace.get(name)
                    if (dtype := annotations.get(name)):
                        if not getattr(dtype, '__name__', '') == 'Field':
                            raise exceptions.FieldAnnotationeError(name, dtype)
                        else:
                            default['type'] = typing.get_args(dtype)[0]
                    else:
                        raise exceptions.MissingTypeAnnotation(name)
                    default['name'] = name
                    fields[name] = default
                    slots.append(name)
                    defaults.append(name)
            for name in defaults:
                __namespace.pop(name)
            for name, dtype in annotations.items():
                if name in fields and name not in base_fields:
                    continue
                elif not utils.is_valid_keyword(name):
                    raise exceptions.ReservedKeywordError(name)
                elif (
                    dtypes.utils.is_classvar(dtype)
                    or dtypes.utils.is_finalvar(dtype)
                    ):
                    continue
                elif not getattr(dtype, '__name__', '') == 'Field':
                    raise exceptions.FieldAnnotationeError(name, dtype)
                elif (
                    (default := __namespace.pop(name, Constants.UNDEFINED))
                    == Constants.UNDEFINED
                    ):
                    required = True
                    default = None
                else:
                    required = False
                if module == Constants.FIELDS_MODULE:
                    field = modules.Modules.fields.Field(  # type: ignore[attr-defined]
                        name=name,
                        type=typing.get_args(dtype)[0],
                        default=default,
                        required=required,
                        )
                else:
                    field = modules.Modules().fields.Field(  # type: ignore[attr-defined]
                        name=name,
                        type=typing.get_args(dtype)[0],
                        default=default,
                        required=required,
                        )
                fields[name] = field
                slots.append(name)

        is_snake_case = (
            utils.is_snake_case(fields)
            if fields
            else False
            )
        isCamelCase = (
            utils.isCamelCase(fields)
            if fields
            else False
            )
        if fields and not (is_snake_case or isCamelCase):
            raise exceptions.IncorrectCasingError(fields)

        namespace = {
            '__slots__': tuple(slots),
            **__namespace,
            }

        namespace['__fields__'] = fields
        namespace['__heritage__'] = heritage
        namespace['__cache__'] = {}
        namespace['fields'] = tuple(
            f
            for f
            in fields
            if utils.is_public_field(f)
            )
        namespace['distribution'] = utils.get_distribution(module)
        namespace['description'] = utils.get_description(
            __name,
            module,
            namespace.get('__doc__')
            )
        namespace['enumerations'] = utils.get_enumerations(fields)
        namespace['hash_fields'] = utils.get_hash_fields(fields)
        namespace['reference'] = utils.get_reference(__name, module)
        namespace['is_snake_case'] = is_snake_case
        namespace['isCamelCase'] = isCamelCase

        return super().__new__(
            mcs,
            __name,
            __bases,
            namespace,
            **kwargs
            )

    def __getattribute__(cls, __name: str) -> typing.Any:
        __fields: dict[str, dtypes.FieldType] = type.__getattribute__(
            cls,
            '__fields__'
            )
        if (field := __fields.get(__name)):
            return field
        else:
            return super().__getattribute__(__name)

    @typing.overload
    def __getitem__(cls: type['fields_.Field'], key: type[dtypes.Type]) -> 'fields_.Field[dtypes.Type]': ...  # type: ignore[misc]  # noqa
    @typing.overload
    def __getitem__(cls: type['fields_.Field'], key: str) -> '_fields.Field': ...  # type: ignore[misc, overload-overlap]  # noqa
    @typing.overload
    def __getitem__(cls, key: str) -> 'fields_.Field': ...
    def __getitem__(cls, key: typing.Any) -> typing.Union[dtypes.FieldType, 'dtypes.Field']:  # noqa
        """Return Field dict style."""

        if (
            (is_string := isinstance(key, str))
            and (k := utils.key_for(cls, key))
            ):
            return cls.__fields__[k]
        elif not is_string and cls is modules.Modules().fields.Field:  # type: ignore[attr-defined]
            return dtypes.Field(cls, key)
        else:
            raise KeyError(key)

    def __setitem__(cls, key: typing.Any, value: typing.Any) -> None:
        """Set Field for key dict style."""

        if not utils.is_field_type(value):
            raise exceptions.IncorrectTypeError(key, dtypes.FieldType, value)
        elif (
            issubclass(cls, modules.Modules().fields.Field)  # type: ignore[attr-defined]
            and not isinstance(value, modules.Modules.fields.Field)  # type: ignore[attr-defined]
            ):
            raise exceptions.IncorrectTypeError(key, modules.Modules.fields.Field, value)  # type: ignore[attr-defined]
        elif (k := utils.key_for(cls, key)) and value['name'] != k:
            raise exceptions.InvalidFieldRedefinitionError(value['name'])
        elif k and (
            value['type'] != (ftype := cls.__fields__[k]['type'])
            and value['type'] not in getattr(ftype, '__args__', ())
            ):
            raise exceptions.IncorrectTypeError(k, ftype, value['type'])
        elif k and (
            type(value['default']) != ftype
            and type(value['default']) not in getattr(ftype, '__args__', ())
            ):
            raise exceptions.IncorrectDefaultTypeError(k, ftype, value['default'])
        elif k:
            cls.__fields__[k].update(value)
        else:
            raise exceptions.InvalidFieldRedefinitionError(key)

    @typing.overload
    def __iter__(cls: type['fields_.Field']) -> typing.Iterator[tuple[str, '_fields.Field']]: ...  # type: ignore[misc, overload-overlap]  # noqa
    @typing.overload
    def __iter__(cls) -> typing.Iterator[tuple[str, 'fields_.Field']]: ...
    def __iter__(cls) -> typing.Iterator[tuple[str, dtypes.FieldType]]:
        """
        Return an iterator of keys and Fields like a dict.

        ---

        Removes any suffixed underscores from field names (`_`).

        """

        for k, v in Meta.items(cls):
            yield k, v

    def __repr__(cls) -> str:
        """Return object represented as a neatly formatted JSON string."""

        return json.dumps(
            utils.convert_for_representation(cls),
            default=utils.convert_for_representation,
            indent=Constants.INDENT,
            sort_keys=True
            )

    def __instancecheck__(cls, __instance: typing.Any) -> bool:
        """Instance check that considers slotted heritage."""

        return (
            super().__instancecheck__(__instance)
            or cls in getattr(__instance, '__heritage__', ())
            )

    def __subclasscheck__(cls, __subclass: type[typing.Any]) -> bool:
        """Subclass check that considers slotted heritage."""

        return (
            super().__subclasscheck__(__subclass)
            or cls in getattr(__subclass, '__heritage__', ())
            )

    @typing.overload
    def get(  # type: ignore[misc]
        cls: type['fields_.Field'],
        key: type[dtypes.Type],
        default: typing.Optional[dtypes.Default] = None
        ) -> typing.Union['fields_.Field[dtypes.Type]', dtypes.Default]: ...  # noqa
    @typing.overload
    def get(
        cls,
        key: str,
        default: typing.Optional[dtypes.Default] = None
        ) -> typing.Union['fields_.Field', dtypes.Default]: ...
    def get(
        cls,
        key: typing.Any,
        default: typing.Optional[dtypes.Default] = None
        ) -> typing.Union[dtypes.FieldType, dtypes.Default]:
        """Return Field by key if exists, otherwise default."""

        if (k := utils.key_for(cls, key)):
            return cls[k]
        else:
            return default

    @typing.overload
    def items(cls: type['fields_.Field']) -> typing.Iterator[tuple[str, '_fields.Field']]: ...  # type: ignore[misc, overload-overlap]  # noqa
    @typing.overload
    def items(cls) -> typing.Iterator[tuple[str, 'fields_.Field']]: ...
    def items(cls) -> typing.Union[typing.Iterator[tuple[str, 'fields_.Field']], typing.Iterator[tuple[str, '_fields.Field']]]:  # noqa
        """
        Return an iterator of keys and Fields like a dict.

        ---

        Removes any suffixed underscores from field names (`_`).

        """

        for name in cls.__fields__:
            yield name.removesuffix('_'), cls[name]

    def update(cls, other: dtypes.MetaType) -> None:
        """Update fields like a dict."""

        for k, v in Meta.items(other):
            if utils.key_for(cls, k):
                cls[k] = v

    @typing.overload
    def values(cls: type['fields_.Field']) -> typing.Iterator['_fields.Field']: ...  # type: ignore[misc]  # noqa
    @typing.overload
    def values(cls: type['Base']) -> typing.Iterator['fields_.Field']: ...  # type: ignore[misc]
    def values(cls) -> typing.Union[typing.Iterator['fields_.Field'], typing.Iterator['_fields.Field']]:  # noqa
        """Return an iterator of Fields like a dict."""

        for name in cls.__fields__:
            yield cls[name]


class Base(metaclass=Meta):
    """Internal base."""

    if typing.TYPE_CHECKING:
        __fields__: typing.ClassVar[typing.Mapping[str, dtypes.FieldType]] = {}
        __heritage__: typing.ClassVar[tuple[type['Base'], ...]] = ()
        __cache__: typing.ClassVar[dict[str, typing.Any]] = {}

        description: typing.ClassVar[str] = Constants.UNDEFINED
        distribution: typing.ClassVar[str] = Constants.UNDEFINED
        enumerations: typing.ClassVar[dict[str, list]] = {}
        fields: typing.ClassVar[tuple[str, ...]] = ()
        hash_fields: typing.ClassVar[tuple[str, ...]] = ()
        reference: typing.ClassVar[str] = Constants.UNDEFINED
        is_snake_case: typing.ClassVar[bool] = True
        isCamelCase: typing.ClassVar[bool] = False

    __slots__: typing.ClassVar[tuple[str, ...]] = ()

    def __init__(
        self,
        class_as_dict: typing.Optional[dict[str, typing.Any]] = None,
        /,
        **kwargs: typing.Any
        ):
        kwargs.update(class_as_dict or {})
        for name, field in self.__fields__.items():
            self[name] = kwargs.get(
                name,
                (
                    field['default']()
                    if callable(field['default'])
                    else field['default']
                    if field['type'] in typing.get_args(dtypes.Immutable)
                    else copy.deepcopy(field['default'])
                    )
                )
        for name, default in kwargs.items():
            self[name] = default
        self.__post_init__()

    def __post_init__(self) -> None:
        """Method that will always run after instantiation."""

    def __getitem__(self, key: str) -> typing.Any:
        """Return field value dict style."""

        if (k := utils.key_for(self, key)):
            return getattr(self, k)
        else:
            raise KeyError(key)

    def __setitem__(self, key: str, value: typing.Any) -> None:
        """Set field value dict style."""

        if (k := utils.key_for(self, key)):
            setattr(self, k, value)
        else:
            raise exceptions.InvalidFieldRedefinitionError(key)

    def __iter__(self) -> typing.Iterator[tuple[str, typing.Any]]:
        """
        Return an iterator of keys and values like a dict.

        ---

        Removes any suffixed underscores from field names (`_`).

        """

        for k, v in self.items():
            yield k, v

    def __contains__(self, key: str) -> bool:
        """Return True if key (or alias) is a field for the derivative."""

        return bool(utils.key_for(self, key))

    def __len__(self) -> int:
        """Return count of fields."""

        return len(self.__fields__)

    def __repr__(self) -> str:
        """Return object represented as a neatly formatted JSON string."""

        return json.dumps(
            utils.convert_for_representation(self),
            default=utils.convert_for_representation,
            indent=Constants.INDENT,
            sort_keys=True
            )

    def __hash__(self) -> int:
        return hash(
            Constants.DELIM.join(
                [
                    '.'.join((k, str(v)))
                    for k
                    in self.hash_fields
                    if (v := self[k])
                    ]
                )
            )

    def __bool__(self) -> bool:
        """Determine truthiness by diff with default field values."""

        return bool(self - self.__class__())

    def __eq__(self, other: object) -> bool:

        return hash(self) == hash(other)

    def __ne__(self, other: object) -> bool:

        return hash(self) != hash(other)

    def __sub__(
        self: dtypes.BaseType,
        other: dtypes.BaseType
        ) -> dict[str, typing.Any]:
        """Calculate diff between same object types."""

        diff = {}
        for field in self.__fields__:
            if self[field] != other[field]:
                diff[field] = other[field]
        return diff

    def __lshift__(
        self: dtypes.BaseType,
        other: dtypes.BaseType
        ) -> dtypes.BaseType:
        """
        Interpolate values from other if populated with non-default \
        and return a new instance without mutating self or other.

        """

        object_ = self.__class__()
        for field, __field in self.__fields__.items():
            if (
                self[field] == __field['default']
                and other[field] != __field['default']
                ):
                object_[field] = other[field]
            else:
                object_[field] = self[field]
        return object_

    def __rshift__(
        self: dtypes.BaseType,
        other: dtypes.BaseType
        ) -> dtypes.BaseType:
        """
        Overwrite values from other if populated with non-default \
        and return a new instance without mutating self or other.

        """

        object_ = self.__class__()
        for field, __field in self.__fields__.items():
            if other[field] != __field['default']:
                object_[field] = other[field]
            else:
                object_[field] = self[field]
        return object_

    def __getstate__(self) -> dict[str, typing.Any]:
        return {'__values__': dict(self)}

    def __setstate__(
        self,
        state: dict[str, typing.Union[dict, typing.Any]]
        ) -> None:
        self.update(state['__values__'])

    def get(
        self,
        key: str,
        default: dtypes.Default = None
        ) -> typing.Union[typing.Any, dtypes.Default]:
        """Return value by key if exists, otherwise default."""

        if (k := utils.key_for(self, key)):
            return self[k]
        else:
            return default

    def items(self) -> typing.Iterator[tuple[str, typing.Any]]:
        """
        Return an iterator of keys and values like a dict.

        ---

        Removes any suffixed underscores from field names (`_`).

        """

        for k, v in self.to_dict().items():
            yield k, v

    @classmethod
    def keys(cls) -> typing.Iterator[str]:
        """
        Return an iterator of keys like a dict.

        ---

        Removes any suffixed underscores from field names (`_`).

        """

        for field in cls.__fields__:
            yield field.removesuffix('_')

    def setdefault(self, key: str, value: typing.Any) -> None:
        """Set value for key if unset; otherwise do nothing."""

        if (
            (k := utils.key_for(self, key))
            and (
                (
                    __value := self.get(k, Constants.UNDEFINED)
                    ) == Constants.UNDEFINED
                or __value == self.__fields__[k]['default']
                )
            ):
            self[k] = value
        elif not k:
            raise exceptions.InvalidFieldRedefinitionError(key)

    def update(self, other: typing.Union[dtypes.BaseType, dict]) -> None:
        """Update values like a dict."""

        for k, v in other.items():
            if utils.key_for(self, k):
                self[k] = v

    def values(self) -> typing.Iterator[typing.Any]:
        """Return an iterator of values like a dict."""

        for field in self.__fields__:
            yield self[field]

    def to_dict(
        self,
        camel_case: bool = False,
        include_null: bool = True,
        ) -> dict:
        """
        Same as `dict(Object)`, but gives fine-grained control over \
        casing and inclusion of `null` values.

        ---

        If specified, keys may optionally be converted to camelCase.

        `None` values may optionally be discarded as well.

        ---

        Removes any suffixed underscores from field names (`_`).

        """

        d = {
            k: v
            for k
            in self.__fields__
            if (v := self[k]) is not None
            or (include_null and v is None)
            }
        dbo: dict[str, typing.Any] = {}
        for k, v in d.items():
            if isinstance(v, Base):
                dbo[k] = v.to_dict(camel_case, include_null)
            elif isinstance(v, dict):
                dbo[k] = {
                    (
                        utils.to_camel_case(_k.strip('_'))
                        if (camel_case and isinstance(_k, str))
                        else _k
                        ): (
                            _v.to_dict(camel_case, include_null)
                            if isinstance(_v, Base)
                            else
                            _v
                            )
                    for _k, _v
                    in v.items()
                    if utils.is_public_field(_k)
                    and (
                        _v is not None
                        if not include_null
                        else True
                        )
                    }
            elif isinstance(v, typing.get_args(dtypes.Array)):
                dbo[k] = v.__class__(
                    _v.to_dict(camel_case, include_null)
                    if isinstance(_v, Base)
                    else
                    _v
                    for _v
                    in v
                    if (
                        _v is not None
                        if not include_null
                        else True
                        )
                    )
            else:
                dbo[k] = v
        if camel_case:
            dbo = {
                utils.to_camel_case(k.strip('_')): v
                for k, v
                in dbo.items()
                }
        else:
            dbo = {
                k.removesuffix('_'): v
                for k, v
                in dbo.items()
                }
        return dbo
