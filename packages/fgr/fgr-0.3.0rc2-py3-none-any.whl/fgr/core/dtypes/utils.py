__all__ = (
    'is_classvar',
    'is_finalvar',
    'parse_type',
    'parse_type_args',
    'resolve_annotations',
    'resolve_type',
    )

import typing

from . import constants


class Constants(constants.TypeConstants):

    pass


_eval_type: typing.Callable[
    [
        typing.Any,
        typing.Any,
        typing.Any,
        typing.Optional[frozenset]
        ],
    type[typing.Any]
    ] = getattr(typing, '_eval_type')


def parse_type(
    dtype: typing.Union[type[typing.Any], typing.ForwardRef, str],
    __globals: typing.Optional[dict[str, typing.Any]] = None,
    __locals: typing.Optional[dict[str, typing.Any]] = None
    ) -> typing.Union[type[typing.Any], typing.ForwardRef]:
    """Attempt to cast str or ForwardRef to type."""

    if isinstance(dtype, str):
        dtype = typing.ForwardRef(dtype, is_argument=False, is_class=True)

    try:
        dtyped: type[typing.Any] = _eval_type(
            dtype,
            __globals,
            __locals,
            frozenset()
            )
        return dtyped
    except NameError:
        pass

    return dtype


def parse_type_args(
    tp: typing.Union[type[typing.Any], typing.ForwardRef, str]
    ) -> typing.Union[type[typing.Any], typing.ForwardRef, str]:
    """Replace string type hints in Generics with ForwardRefs."""

    if not (
        typing.get_origin(tp)
        and getattr(tp, '__args__', None)
        ):
        return tp

    for arg in typing.get_args(tp):
        parse_type_args(arg)

    return tp


def resolve_annotations(
    __annotations: dict[str, typing.Union[type[typing.Any], str]],
    __globals: typing.Optional[dict[str, typing.Any]] = None
    ) -> dict[str, typing.Union[type[typing.Any], typing.ForwardRef]]:
    """Resolve annotation strings or ForwardRefs to type objects."""

    annotations = {}
    for name, _dtype in __annotations.items():
        annotations[name] = resolve_type(_dtype, __globals)
    return annotations


def resolve_type(
    tp: typing.Union[type[typing.Any], typing.ForwardRef, str],
    __globals: typing.Optional[dict[str, typing.Any]] = None,
    __locals: typing.Optional[dict[str, typing.Any]] = None
    ) -> typing.Union[type[typing.Any], typing.ForwardRef]:
    """Attempt to resolve str or ForwardRef to type."""

    tp = parse_type_args(tp)
    return parse_type(tp, __globals, __locals)


def _check_classvar(
    v: typing.Union[type[typing.Any], typing.ForwardRef]
    ) -> bool:
    return (
        v.__class__ == typing.ClassVar.__class__
        and getattr(v, '_name', '') == 'ClassVar'
        )


def _check_finalvar(
    v: typing.Union[type[typing.Any], typing.ForwardRef]
    ) -> bool:
    return (
        v.__class__ == typing.Final.__class__
        and getattr(v, '_name', '') == 'Final'
        )


def is_classvar(
    dtype: typing.Union[type[typing.Any], typing.ForwardRef]
    ) -> bool:
    """Return True if annotation is a ClassVar."""

    return (
        (
            _check_classvar(dtype)
            or _check_classvar(typing.get_origin(dtype))
            )
        or (
            dtype.__class__ == typing.ForwardRef
            and getattr(dtype, '__forward_arg__', '').startswith('ClassVar[')
            )
        )


def is_finalvar(
    dtype: typing.Union[type[typing.Any], typing.ForwardRef]
    ) -> bool:
    """Return True if annotation is a FinalVar."""

    return (
        _check_finalvar(dtype)
        or _check_finalvar(typing.get_origin(dtype))
        )
