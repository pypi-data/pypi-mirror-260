__all__ = (
    'Modules',
    )

import functools
import importlib
import sys
import types
import typing

from . import constants
from . import dtypes

if typing.TYPE_CHECKING:
    from . import _fields
    from . import fields
    from . import meta
    from . import query


class Constants(constants.PackageConstants):  # noqa

    pass


@functools.lru_cache(maxsize=4)
def _import(module: str) -> types.ModuleType:
    m = importlib.import_module(
        '.' + module,
        '.'.join((Constants.PACAKGE, 'core'))
        )
    if module.endswith('meta'):
        dtypes.ValidLogType = dtypes.utils.resolve_type(  # type: ignore[assignment]
            dtypes.ValidLogType,  # type: ignore[arg-type]
            sys.modules['.'.join((Constants.PACAKGE, 'core'))].__dict__,
            m.__dict__
            )
    elif module.endswith('query'):
        dtypes.Query = dtypes.utils.resolve_type(  # type: ignore[assignment]
            dtypes.Query,  # type: ignore[arg-type]
            sys.modules['.'.join((Constants.PACAKGE, 'core'))].__dict__,
            m.__dict__
            )
    elif module.endswith('fields'):
        dtypes.FieldType = dtypes.utils.resolve_type(  # type: ignore[assignment]
            dtypes.FieldType,  # type: ignore[arg-type]
            sys.modules['.'.join((Constants.PACAKGE, 'core'))].__dict__,
            m.__dict__
            )
    return m


class Fields:  # noqa

    @typing.overload
    def __get__(
        self,
        object_: None,
        dtype: type['Modules']
        ) -> '_fields': ...  # type: ignore[valid-type]
    @typing.overload
    def __get__(
        self,
        object_: 'Modules',
        dtype: type['Modules']
        ) -> 'fields': ...  # type: ignore[valid-type]
    def __get__(
        self,
        object_: typing.Optional['Modules'],
        dtype: type['Modules']
        ) -> types.ModuleType:
        prefix = '' if object_ else '_'
        return _import(prefix + self.__class__.__name__.lower())


class Meta:  # noqa

    @typing.overload
    def __get__(
        self,
        object_: None,
        dtype: type['Modules']
        ) -> None: ...
    @typing.overload
    def __get__(
        self,
        object_: 'Modules',
        dtype: type['Modules']
        ) -> 'meta': ...  # type: ignore[valid-type]
    def __get__(
        self,
        object_: typing.Optional['Modules'],
        dtype: type['Modules']
        ) -> typing.Optional[types.ModuleType]:
        if object_:
            return _import(self.__class__.__name__.lower())
        else:  # pragma: no cover
            return None


class Query:  # noqa

    @typing.overload
    def __get__(
        self,
        object_: None,
        dtype: type['Modules']
        ) -> None: ...
    @typing.overload
    def __get__(
        self,
        object_: 'Modules',
        dtype: type['Modules']
        ) -> 'query': ...  # type: ignore[valid-type]
    def __get__(
        self,
        object_: typing.Optional['Modules'],
        dtype: type['Modules']
        ) -> typing.Optional[types.ModuleType]:
        if object_:
            return _import(self.__class__.__name__.lower())
        else:  # pragma: no cover
            return None


class Modules:
    """
    Helper to avoid circular imports.

    Instantiate to return `public_modules`, otherwise \
    class attributes will return `_private_modules` or \
    `None` if a module is not yet available.

    """

    __singleton = None

    def __new__(cls) -> 'Modules':
        if cls.__singleton is None:
            cls.__singleton = super().__new__(cls)
        return cls.__singleton

    fields = Fields()
    meta = Meta()
    query = Query()
