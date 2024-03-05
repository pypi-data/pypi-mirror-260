"""
Centralized application log.

Pre-configured so you do not need to. By default, this loggger \
will do everything it can to keep your log stream as actionable \
and free from pollution as possible.

* emits neatly formatted JSON log messages
* intercepts forgotten print statements
    \
    * silences them in all deployed environments
* intercepts forgotten debug-level logs
    \
    * silences them in deployed environments > dev
* intercepts irritating warnings, displaying them once as \
neatly formatted warning level log messages
* automatically redacts things that should never be logged \
in the first place (like API Keys, credentials, SSN's, etc.)

---

Usage
-----

The expectation is this will be the only log used across \
an application.

* Set logging level through the `LOG_LEVEL` environment variable.
    \
    * Defaults to 'DEBUG' if `Constants.ENV` is either `local` (default) \
    or `dev`, otherwise 'INFO'.

---

Special Rules
-------------

* Can only log `str`, `dict`, and `Object` types.

* Automatically redacts almost all sensitive data, including \
api keys, tokens, credit card numbers, connection strings, \
and secrets.

* All `warnings` will be filtered through this log and \
displayed only once.

* All `print` statements will be silenced *except* when \
`Constants.ENV` is set to 'local' (its default if `ENV` \
is unavailable in `os.environ` at runtime).
    \
    * Best practice is to set log level to 'DEBUG' and \
    use the `log.debug` method in place of `print` statements.
    \
    * `warnings` will be displayed once for all `print` \
    statements that would otherwise be silenced in any \
    non-local development environment.

---

Usage Examples
--------------

```py
import fgr
.log.debug('example')
# >>>
# {
#   "level": DEBUG,
#   "time": 2024-02-25 15:30:01.061 UTC,
#   "log": fgr.core.log,
#   "data":   {
#     "message": "example"
#   }
# }
.log.info({'str': 'example', 'a': 2})
# >>>
# {
#   "level": INFO,
#   "time": 2024-02-25 15:31:11.118 UTC,
#   "log": fgr.core.log,
#   "data":   {
#     "a": 2,
#     "str": "example"
#   }
# }


class Pet(fgr.Object):
    \"""A pet.\"""

    id_: fgr.Field[str]
    _alternate_id: fgr.Field[str]

    name: fgr.Field[str]
    type: fgr.Field[str]
    in_: fgr.Field[str]
    is_tail_wagging: fgr.Field[bool] = True

.log.debug(Pet)
# >>>
# {
#   "level": DEBUG,
#   "time": 2024-02-25 15:30:01.339 UTC,
#   "log": fgr.core.log,
#   "data":   {
#     "Pet": {
#       "_alternate_id": "Field[str]",
#       "id_": "Field[str]",
#       "in_": "Field[str]",
#       "is_tail_wagging": "Field[bool]",
#       "name": "Field[str]",
#       "type": "Field[str]"
#     }
#   }
# }
.log.debug(
    Pet(
        id_='abc1234',
        name='Fido',
        type='dog',
        )
    )
# >>>
# {
#   "level": DEBUG,
#   "time": 2024-02-25 15:30:01.450 UTC,
#   "log": fgr.core.log,
#   "data":   {
#     "Pet": {
#       "_alternate_id": null,
#       "id_": "abc1234",
#       "in_": null,
#       "is_tail_wagging": true,
#       "name": "Fido",
#       "type": "dog"
#     }
#   }
# }

```

"""

__all__ = (
    'critical',
    'debug',
    'error',
    'info',
    'warning',
    )

import functools
import json
import logging
import sys
import textwrap
import time
import traceback
import typing
import warnings

from . import constants
from . import utils


class Constants(constants.PackageConstants):  # noqa

    pass


@functools.lru_cache(maxsize=1)
def _log() -> logging.Logger:
    """
    Cached function that will always return the same, \
    centralized logger, configuring it on the first call.

    """

    logging.Formatter.converter = time.gmtime
    logging.Formatter.default_time_format = Constants.FTIME_LOG
    logging.Formatter.default_msec_format = Constants.FTIME_LOG_MSEC
    logging.basicConfig(
        format=(' ' * Constants.INDENT).join(
            (
                '{\n',
                '"level": %(levelname)s,\n',
                '"time": %(asctime)s,\n',
                '"log": %(name)s,\n',
                '"data": %(message)s}',
                )
            ),
        )

    log = logging.getLogger(__name__)
    log.setLevel(logging._nameToLevel[Constants.LOG_LEVEL])

    warnings.simplefilter('once')
    logging.captureWarnings(True)
    logging.Logger.manager.loggerDict['py.warnings'] = log

    _print = __builtins__['print']  # type: ignore[index]

    def _reprint(*args: typing.Any, **kwargs: typing.Any) -> None:
        if Constants.ENV in Constants.DEPLOY_ENVS:
            warnings.warn(
                '\n'.join(
                    (
                        Constants.SILENCE_MSG,
                        *[str(a) for a in args],
                        )
                    ),
                stacklevel=1
                )
        else:
            warnings.warn(Constants.WARN_MSG, stacklevel=1)
            _print(*args, **kwargs)

    __builtins__['print'] = _reprint

    def _custom_log(
        level: int,
        msg: typing.Any,
        args: 'logging._ArgsType',
        exc_info: 'logging._ExcInfoType' = True,
        extra: typing.Union[typing.Mapping[str, object], None] = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        **kwargs: typing.Any
        ) -> None:
        sinfo = None
        if logging._srcfile:  # pragma: no cover
            try:
                fn, lno, func, sinfo = log.findCaller(stack_info, stacklevel)
            except ValueError:
                fn, lno, func = "(unknown file)", 0, "(unknown function)"
        else:  # pragma: no cover
            fn, lno, func = "(unknown file)", 0, "(unknown function)"

        if msg == '%s' and args and isinstance(args, tuple):  # pragma: no cover
            msg = args[0]

        msg = utils.parse_incoming_log_message(msg, level)

        if isinstance(exc_info, BaseException):
            exc_info = (type(exc_info), exc_info, exc_info.__traceback__)
        elif not isinstance(exc_info, tuple):
            exc_info = sys.exc_info()
        if (
            exc_info[-1] is not None
            and not isinstance(exc_info[1], KeyboardInterrupt)
            ):
            msg['traceback'] = traceback.format_exc()

        record = log.makeRecord(
            log.name,
            level,
            fn,
            lno,
            textwrap.indent(
                json.dumps(
                    utils.convert_for_representation(msg),
                    default=utils.convert_for_representation,
                    indent=Constants.INDENT,
                    sort_keys=True
                    ) + '\n',
                Constants.INDENT * ' '
                ),
            tuple(),
            None,
            func,
            extra,
            sinfo
            )
        log.handle(record)

    log._log = _custom_log  # type: ignore[method-assign]
    return log


critical = _log().critical
debug = _log().debug
error = _log().error
info = _log().info
warning = _log().warning
