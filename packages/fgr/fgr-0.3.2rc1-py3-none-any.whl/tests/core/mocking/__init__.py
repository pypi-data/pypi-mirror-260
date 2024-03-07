import datetime
import decimal
import typing

import fgr

from . import examples


class Derivative(fgr.Object):
    """Simple test derivative."""

    secondary_key: fgr.Field[int] = 123
    str_field: fgr.Field[str] = 'abc'
    bool_field: fgr.Field[bool] = True
    int_field: fgr.Field[int] = 2
    forward_ref_alias_field: 'fgr.Field[fgr.core.dtypes.GenericType]' = 2
    forward_ref_union_field: 'fgr.Field[typing.Union[int, str, tuple[int | str, ...]]]' = 2  # noqa
    forward_ref_field: fgr.Field[list['Derivative']] = []
    enumerated_bool_field: fgr.Field[bool] = fgr.Field(
        default=False,
        enum=fgr.core.enums.Boolean,
        )
    from_dict_field: fgr.Field[str] = {
        'default': 'asc',
        'enum': {'asc', 'desc'},
        'nullable': False,
        'required': False
        }
    null_field: fgr.Field[fgr.core.dtypes.NoneType] = None
    non_nullable_field: fgr.Field[str] = fgr.Field(
        default='not_null',
        type=str,
        nullable=False,
        )
    required_field: fgr.Field[int]
    date_field: fgr.Field[datetime.date] = (
        lambda: datetime.datetime.now(datetime.timezone.utc).date()
        )
    datetime_field: fgr.Field[datetime.datetime] = (
        lambda: datetime.datetime.now(datetime.timezone.utc)
        )
    decimal_field: fgr.Field[decimal.Decimal] = decimal.Decimal(1e-3)
    tuple_field: fgr.Field[tuple] = (1, 2)
    generic_tuple_field: fgr.Field[tuple[str]] = ('a', 'b')


class DubDeriv(Derivative):

    test_again: fgr.Field[bool] = True
    bob: fgr.Field[str] = 'Dan'
    other_field: fgr.Field[str] = fgr.Field(
        default='Paul',
        enum=['Paul']
        )

    def do_stuff(self):
        ...


class MixinDeriv(fgr.Object):

    test_again: fgr.Field[bool] = True
    bob: fgr.Field[str] = 'David'
    other_field: fgr.Field[str] = fgr.Field(
        default='Albert',
        enum=['Albert']
        )

    def do_stuff(self):
        ...


class NewDeriv(fgr.Object):

    anti_field_1: fgr.Field[str] = 'cba'
    anti_field_2: fgr.Field[bool] = False
    generic_tuple_deriv_field: fgr.Field[tuple[MixinDeriv, ...]] = lambda: (
        MixinDeriv(bob='Frank'),
        MixinDeriv(bob='Bob'),
        )


class TripDeriv(MixinDeriv, DubDeriv):

    test_another: fgr.Field[bool] = False
    new_deriv: fgr.Field[NewDeriv] = NewDeriv()
    dict_field: fgr.Field[dict] = {'record_id': 123}
    generic_dict_field: fgr.Field[dict[str, str]] = {'record_id': '123'}


class AntiTripDeriv(DubDeriv, MixinDeriv):

    test_another: fgr.Field[bool] = False
    new_deriv: fgr.Field[NewDeriv] = NewDeriv()
    dict_field: fgr.Field[dict] = {'record_id': 321}
    generic_dict_field: fgr.Field[dict[str, str]] = {'record_id': '123'}
