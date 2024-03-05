__all__ = (
    'Boolean',
    'MatchThreshold',
    'SortDirection',
    )

import enum

from . import constants


class Constants(constants.PackageConstants):  # noqa

    pass


class Boolean(enum.Enum):

    true  = True
    false = False


class MatchThreshold(enum.Enum):
    """Enumeration for default similarity query threshold."""

    default = 0.85


class SortDirection(enum.Enum):
    """Enumeration for valid sort directions."""

    asc  = 'asc'
    desc = 'desc'
