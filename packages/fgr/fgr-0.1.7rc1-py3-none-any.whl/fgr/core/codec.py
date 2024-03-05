__all__ = (
    'encode',
    )

import collections
import datetime
import decimal
import enum
import ipaddress
import pathlib
import re
import types
import typing
import uuid

from . import constants
from . import dtypes


class Constants(constants.PackageConstants):  # noqa

    pass


def _isoformat_encoder(o: typing.Union[datetime.date, datetime.time]) -> str:
    return o.isoformat()


ENCODERS: dict[
    type[typing.Any],
    typing.Callable[[typing.Any], dtypes.Serial]
    ] = {
        bytes: lambda o: getattr(o, 'decode')(),
        datetime.date: _isoformat_encoder,
        datetime.datetime: _isoformat_encoder,
        datetime.time: _isoformat_encoder,
        datetime.timedelta: lambda td: getattr(td, 'total_seconds')(),
        decimal.Decimal: float,
        enum.Enum: lambda o: getattr(o, 'value'),
        frozenset: list,
        collections.deque: list,
        types.GeneratorType: list,
        ipaddress.IPv4Address: str,
        ipaddress.IPv4Interface: str,
        ipaddress.IPv4Network: str,
        ipaddress.IPv6Address: str,
        ipaddress.IPv6Interface: str,
        ipaddress.IPv6Network: str,
        pathlib.Path: str,
        re.Pattern: lambda o: getattr(o, 'pattern'),
        set: list,
        uuid.UUID: str,
        }


def encode(object_: typing.Any) -> dtypes.Serial:
    """JSON encode object using corresponding encoder, else repr."""

    for base in object_.__class__.__mro__[:-1]:
        try:
            encoder = ENCODERS[base]
        except KeyError:
            continue
        else:
            return encoder(object_)
    else:
        return repr(object_)
