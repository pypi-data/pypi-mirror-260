import os


class PackageConstants:
    """Constant values across all of fgr."""

    PACAKGE        = 'fgr'
    BASE_VERSION   = '0.0.0'
    ENV            = os.getenv('ENV', 'local').lower()

    UNDEFINED      = f'[[{PACAKGE.upper()}.DEFAULT.PLACEHOLDER]]'

    DEPLOY_ENVS    = {
        'dev',
        'develop',
        'qa',
        'test',
        'testing',
        'stg',
        'stage',
        'staging',
        'uat',
        'prod',
        'production',
        }

    BASE_ATTRS     = (
        '__cache__',
        '__fields__',
        '__heritage__',
        'description',
        'distribution',
        'enumerations',
        'fields',
        'hash_fields',
        'is_snake_case',
        'isCamelCase',
        'reference',
        )
    DELIM          = '-'
    DELIM_REBASE   = '_X_'
    FTIME_DEFAULT  = '%Y-%m-%dT%H:%M:%S.%f%z'
    FTIME_LOG      = '%Y-%m-%d %H:%M:%S'
    FTIME_LOG_MSEC = '%s.%03d UTC'
    FTIME_US_YEAR  = '%Y-%m-%d'
    FIELD_KEYS     = {
        'default',
        'enum',
        'name',
        'nullable',
        'required',
        'type',
        }
    FORBIDDEN_KEYWORDS = {
        '__init__',
        '__init_subclass__',
        '__new__',
        '__cache__',
        '__hash__',
        '__getattribute__',
        '__bool__',
        '__contains__',
        '__getitem__',
        '__setitem__',
        '__eq__',
        '__ne__',
        '__iter__',
        '__len__',
        '__repr__',
        '__sub__',
        '__lshift__',
        '__rshift__',
        '__getstate__',
        '__setstate__',
        '__instancecheck__',
        '__subclasscheck__',
        'description',
        'distribution',
        'enumerations',
        'fields',
        'get',
        'hash_fields',
        'isCamelCase',
        'is_snake_case',
        'items',
        'keys',
        'reference',
        'setdefault',
        'update',
        'values',
        }

    LOG_LEVEL      = os.getenv(
        'LOG_LEVEL',
        'DEBUG' if ENV in {'dev', 'develop', 'local'} else 'INFO'
        ).upper()
    SILENCE_MSG    = f'Call to print() silenced by {PACAKGE}.'
    WARN_MSG       = f'Calls to print() will be silenced by {PACAKGE}.'

    INDENT         = int(os.getenv('LOG_INDENT', 2))
    LOG_MAX_CHARS  = int(os.getenv('LOG_MAX_CHARS', 256))
    LOG_CUTOFF_LEN = int(os.getenv('LOG_CUTOFF_LEN', 12))
    LOG_WRAP_WIDTH = int(os.getenv('LOG_WRAP_WIDTH', 64))
    M_LINE_TOKEN   = '[[MULTI.LINE.STRING.AS.ARRAY]]'

    FIELDS_MODULE  = '.'.join((PACAKGE, 'core', 'fields'))
    META_MODULE    = '.'.join((PACAKGE, 'core', 'meta'))
