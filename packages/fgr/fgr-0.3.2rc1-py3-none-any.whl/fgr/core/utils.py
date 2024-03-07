__all__ = (
    'camel_case_to_kebab_case',
    'camel_case_to_snake_case',
    'convert_for_representation',
    'convert_string_for_representation',
    'get_description',
    'get_default_description',
    'get_distribution',
    'get_enumerations',
    'get_hash_fields',
    'get_reference',
    'is_array_type',
    'is_field_type',
    'is_primitive',
    'is_public_field',
    'is_snake_case',
    'is_valid_keyword',
    'isCamelCase',
    'key_for',
    'parse_incoming_log_message',
    'redact_dict_string',
    'redact_string',
    'to_camel_case',
    'snake_case_to_kebab_case',
    )

import enum
import functools
import logging
import re
import textwrap
import typing

from . import codec
from . import constants
from . import dtypes
from . import exceptions
from . import modules
from . import patterns


class Constants(constants.PackageConstants):  # noqa

    REDACT_DICT_KEY_PATTERNS = [
        dtypes.RePatternDict(
            ID='api-key-token',
            Severity='HIGH',
            Title='API Key',
            Regex=re.compile(r"""(?i)(api|secret)+([\S]*[\W_]+)?(key|token)"""),  # noqa
            ),
        dtypes.RePatternDict(
            ID='authorization-header',
            Severity='HIGH',
            Title='Authorization Header',
            Regex=re.compile(r"""(?i)(authorization|bearer)+"""),
            ),
        ]
    REDACT_LOG_STR_PATTERNS  = [
        dtypes.RePatternDict(
            ID='conn-string-password',
            Severity='HIGH',
            Title='Connection String Password',
            Regex=re.compile(r"""(:\/\/)+\w+(:[^:@]+)@"""),
            ),
        dtypes.RePatternDict(
            ID='credit-card',
            Severity='HIGH',
            Title='Credit Card',
            Regex=re.compile(r"""\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|6(?:011|5[0-9]{2})[0-9]{12}|(?:2131|1800|35\d{3})\d{11})\b"""),  # noqa
            ),
        *patterns.REDACTION_PATTERNS
        ]


wrapper = textwrap.TextWrapper(
    width=Constants.LOG_WRAP_WIDTH,
    break_long_words=True,
    break_on_hyphens=True,
    max_lines=Constants.LOG_CUTOFF_LEN,
    expand_tabs=False,
    replace_whitespace=True,
    drop_whitespace=False,
    )


@functools.cache
def is_public_field(f: str) -> bool:
    """Return if field name is public."""

    return not (
        (f in Constants.FORBIDDEN_KEYWORDS)
        or (
            f.startswith('_')
            and not f.removesuffix('_').lower().endswith('id')
            )
        )


@functools.cache
def is_valid_keyword(f: str) -> bool:
    """Return if field name is allowed."""

    return f not in (
        Constants.FORBIDDEN_KEYWORDS
        | set(Constants.BASE_ATTRS)
        )


def parse_incoming_log_message(
    msg: dtypes.ValidLogType,
    level: int
    ) -> dict[str, dtypes.ValidLogType]:
    """
    Parse incoming log message or warning to dict format.

    Raises an exception if msg type cannot be parsed.

    """

    if isinstance(msg, str):
        if level != logging.WARNING:
            msg = {'message': msg}
        else:
            msg, _, warn_msg = msg.partition('.py')
            if warn_msg:
                warn_msg = ':'.join(warn_msg.split(':')[3:]).strip()
                warn_msg, *_ = warn_msg.rpartition('\n')
                if Constants.SILENCE_MSG in warn_msg:
                    warn_msg, _, printed = warn_msg.partition('\n')
                    msg = {
                        'message': warn_msg,
                        'printed': printed
                        }
                else:
                    msg = {'message': warn_msg}
            else:
                msg = {'message': msg}
    elif isinstance(msg, modules.Modules().meta.Meta):  # type: ignore[attr-defined]
        msg = {msg.__name__: msg}
    elif isinstance(msg, modules.Modules().meta.Base):  # type: ignore[attr-defined]
        msg = {msg.__class__.__name__: msg}
    elif not isinstance(msg, dict):
        raise exceptions.InvalidLogMessageTypeError(msg)

    return msg


def redact_dict_string(key: str, value: str) -> str:
    """Redact potentially sensitive value pairs from being logged."""

    for d in Constants.REDACT_DICT_KEY_PATTERNS:
        if d['Regex'].search(key) is not None:
            return f'[ REDACTED :: {d["Title"].upper()} ]'

    return value


def redact_string(string: str) -> str:
    """Redact potentially sensitive values from being logged."""

    for d in Constants.REDACT_LOG_STR_PATTERNS:
        string = d['Regex'].sub(
            repl=f'[ REDACTED :: {d["Title"].upper()} ]',
            string=string
            )

    return string


def convert_string_for_representation(s: str) -> typing.Union[str, list[str]]:
    """Redact sensitive values and truncate overly long strings."""

    s = redact_string(s)
    if len(s) > Constants.LOG_MAX_CHARS:
        return [
            Constants.M_LINE_TOKEN,
            *wrapper.wrap(s)
            ]
    else:
        return s


def convert_for_representation(d: typing.Any) -> typing.Optional[dtypes.Serial]:
    """Recursively prepare dict for neat __repr__."""

    if isinstance(d, str):
        return convert_string_for_representation(d)
    elif is_primitive(d):
        return d
    elif (
        getattr(
            d,
            '__name__',
            getattr(d.__class__, '__name__', '')
            )
        == 'Field'
        ):
        ftype = d['type']
        if (ftypes := typing.get_args(ftype)):
            _delim = (
                ' | '
                if isinstance(ftype, typing._UnionGenericAlias)  # type: ignore[attr-defined]
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
        else:
            return f'Field[{getattr(ftype, "__name__", "Any")}]'
    elif isinstance(d, dict):
        return {
            convert_for_representation(k): (
                convert_for_representation(redact_dict_string(k, v))
                if (isinstance(k, str) and isinstance(v, str))
                else convert_for_representation(v)
                )
            for k, v
            in d.items()
            }
    elif is_array_type(d):
        return list(
            convert_for_representation(v)
            for v
            in d
            )
    elif (
        issubclass(d.__class__, modules.Modules().meta.Base)  # type: ignore[attr-defined]
        or issubclass(d.__class__, modules.Modules().meta.Meta)  # type: ignore[attr-defined]
        ):
        return convert_for_representation(dict(d))
    elif d is None:
        return d
    else:
        return codec.encode(d)


def camel_case_to_kebab_case(camel_case_str: str) -> str:
    """Convert a camelCase string to kebab-case."""

    return snake_case_to_kebab_case(
        camel_case_to_snake_case(camel_case_str)
        )


def snake_case_to_kebab_case(snake_case_str: str) -> str:
    """Convert a snake_case string to kebab-case."""

    return snake_case_str.replace('_', '-')


def camel_case_to_snake_case(camel_case_str: str) -> str:
    """Convert a camelCase string to snake_case."""

    camel_case_str = camel_case_str[0].lower() + camel_case_str[1:]
    _end = len(camel_case_str) - 1
    return ''.join(
        (
            f'_{character.lower()}'
            if (
                (
                    is_candidate := (
                        character.isupper()
                        or character.isnumeric()
                        )
                    )
                and (
                    should_convert := (
                        i < _end
                        and not (
                            (_next := camel_case_str[i + 1]).isupper()
                            or _next.isnumeric()
                            )
                        )
                    )
                )
            else f'_{character}'
            if (
                is_candidate
                and not should_convert
                and camel_case_str[i - 1].islower()
                )
            else character
            for i, character
            in enumerate(camel_case_str)
            )
        )


def is_snake_case(fields: typing.Iterable[str]) -> bool:
    """True if all fields are snake_case."""

    return all(
        f == camel_case_to_snake_case(f)
        for _f
        in fields
        if (f := _f.strip('_'))
        )


def isCamelCase(fields: typing.Iterable[str]) -> bool:
    """
    True if all fields are camelCase.

    Fields that end with 'id' (case insensitive)
    will not be evaluated.
    """

    return all(
        f == to_camel_case(f)
        for _f
        in fields
        if (f := _f.strip('_'))
        )


def to_camel_case(string: str) -> str:
    """Convert a snake_case or kebab-case string to camelCase."""

    string = string[0].lower() + string[1:]
    characters = []
    capitalize = False
    for i, character in enumerate(string):
        if character in {'_', '-'}:
            capitalize = True
        elif capitalize:
            capitalize = False
            characters.append(character.upper())
        elif (
            (
                character.isupper()
                or character.isnumeric()
                )
            and (
                i <= len(string) - 1
                or not string[i + 1].islower()
                )
            ):
            characters.append(character)
        else:
            characters.append(character.lower())

    return ''.join(characters)


def get_hash_fields(fields: dict[str, dtypes.FieldType]) -> tuple[str, ...]:
    """
    Set of minimum fields required to compute a unique hash \
    for the object.

    """

    id_fields: list[str] = []
    name_fields: list[str] = []
    primitive_fields: list[str] = []
    for f, field in fields.items():
        if field['type'] not in typing.get_args(dtypes.Primitive):
            continue
        elif (s := f.strip('_').lower()).endswith('id'):
            id_fields.append(f)
        elif s.endswith('key'):
            id_fields.append(f)
        elif s.startswith('name') or s.endswith('name'):
            name_fields.append(f)
        else:
            primitive_fields.append(f)

    if id_fields:
        return tuple(id_fields)
    elif name_fields:
        return tuple(name_fields)
    elif primitive_fields:
        return tuple(primitive_fields)
    else:
        return tuple(fields)


def get_reference(name: str, module: str) -> str:
    """Get unique reference to the object's name and path."""

    return Constants.DELIM.join(
        (
            *[
                to_camel_case(s)
                for s
                in module.split('.')
                ],
            to_camel_case(name)
            )
        )


def get_distribution(module: str) -> str:
    """The package to which the object belongs."""

    return module.split('.')[0]


def get_description(name: str, module: str, doc: typing.Optional[str]) -> str:
    """
    Brief description of the object.

    ---

    Defaults to the docstring for any derived class, \
    otherwise a one-sentence description of the object's \
    name and membership is generated.

    """

    if doc:
        return doc
    else:
        return get_default_description(name, module)


def get_default_description(name: str, module: str) -> str:
    """Simple description derived from class and package name."""

    return ' '.join(
        (
            'An object called',
            name,
            'belonging to the',
            module,
            'distribution.'
            )
        )


def get_enumerations(fields: dict[str, dtypes.FieldType]) -> dict[str, list]:
    """Dictionary containing all enums for object."""

    d: dict[str, list] = {}
    for k, field in fields.items():
        if isinstance((enum_ := field['enum']), enum.EnumMeta):
            d[k] = [e for e in enum_._member_map_.values()]
        elif isinstance(enum_, typing.get_args(dtypes.Array)):
            d[k] = list(enum_)
        if k in d and field['nullable']:
            d[k].append(None)

    return d


def key_for(
    cls: dtypes.SupportsFields,
    key: typing.Any
    ) -> typing.Optional[str]:
    """
    Get the actual attribute name for key as it has been \
    assigned to the derivative.

    ---

    For example, the below would return '_id', the real \
    field name for the otherwise friendly alias, 'id'.

    ```py
    class Pet(fgr.Object):
        \"""A pet.\"""

        _id: str = None


    Pet.key_for('id')
    >>>
    '_id'

    ```

    """

    cls.__cache__.setdefault('key_mappings', {})
    cache: dict[typing.Any, typing.Optional[str]] = (
        cls.__cache__['key_mappings']
        )
    if key in cache:
        return cache[key]
    elif not isinstance(key, str):
        cls.__cache__['key_mappings'][key] = None
        return None
    elif (
        cls.is_snake_case
        and not key.islower()
        and (
            (
                k := (_k := camel_case_to_snake_case(key.strip('_')))
                ) in cls.__fields__
            or (k := '_' + _k) in cls.__fields__
            or (k := _k + '_') in cls.__fields__
            or (k := '_' + _k + '_') in cls.__fields__
            )
        ):
        cls.__cache__['key_mappings'][key] = k
        return k
    elif (
        (k := (_k := key.strip('_'))) in cls.__fields__
        or (k := '_' + _k) in cls.__fields__
        or (k := _k + '_') in cls.__fields__
        or (k := '_' + _k + '_') in cls.__fields__
        ):
        cls.__cache__['key_mappings'][key] = k
        return k
    else:
        cls.__cache__['key_mappings'][key] = None
        return None


def is_array_type(value: typing.Any) -> typing.TypeGuard[dtypes.Array]:
    """True if Array."""

    return isinstance(value, typing.get_args(dtypes.Array))


def is_field_type(value: typing.Any) -> typing.TypeGuard[dtypes.FieldType]:
    """True if Field."""

    return isinstance(value, typing.get_args(dtypes.FieldType))


def is_primitive(value: typing.Any) -> typing.TypeGuard[dtypes.Primitive]:
    """True if Primitive."""

    return isinstance(value, typing.get_args(dtypes.Primitive))


def _resolve_remaining_type_refs() -> None:
    _ = modules.Modules().query  # type: ignore[attr-defined]
