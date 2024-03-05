import json
import textwrap
import traceback
import unittest
import warnings

import fgr

from . import mocking


class Constants(fgr.core.constants.PackageConstants):  # noqa

    pass


class TestLogger(unittest.TestCase):
    """Fixture for testing logger."""

    def setUp(self) -> None:
        self.log = fgr.log._log()
        self.msg_str = 'example'
        self.msg_dict = {'str': 'example', 'a': 2}
        self.msg_cls = mocking.examples.Pet
        self.msg_object_= mocking.examples.Pet(
            id_='abc1234',
            name='Fido',
            type='dog',
            )
        return super().setUp()

    def test_01_log(self):
        """Test str logging."""

        msg = self.msg_str
        level = fgr.log.logging.DEBUG
        expected_output = textwrap.indent(
            json.dumps(
                fgr.core.utils.parse_incoming_log_message(msg, level),
                default=fgr.core.utils.convert_for_representation,
                indent=Constants.INDENT,
                sort_keys=True
                ) + '\n',
            Constants.INDENT * ' '
            )
        with self.assertLogs(self.log, level) as logger:
            fgr.log.debug(msg)
            self.assertEqual(logger.records[0].msg, expected_output)

    def test_02_log(self):
        """Test dict logging."""

        msg = self.msg_dict
        level = fgr.log.logging.INFO
        expected_output = textwrap.indent(
            json.dumps(
                fgr.core.utils.parse_incoming_log_message(msg, level),
                default=fgr.core.utils.convert_for_representation,
                indent=Constants.INDENT,
                sort_keys=True
                ) + '\n',
            Constants.INDENT * ' '
            )
        with self.assertLogs(self.log, level) as logger:
            fgr.log.info(msg)
            self.assertEqual(logger.records[0].msg, expected_output)

    def test_03_log(self):
        """Test cls logging."""

        msg = self.msg_cls
        level = fgr.log.logging.WARNING
        expected_output = textwrap.indent(
            json.dumps(
                fgr.core.utils.parse_incoming_log_message(msg, level),
                default=fgr.core.utils.convert_for_representation,
                indent=Constants.INDENT,
                sort_keys=True
                ) + '\n',
            Constants.INDENT * ' '
            )
        with self.assertLogs(self.log, level) as logger:
            fgr.log.warning(msg)
            self.assertEqual(logger.records[0].msg, expected_output)

    def test_04_log(self):
        """Test object logging."""

        msg = self.msg_object_
        level = fgr.log.logging.ERROR
        expected_output = textwrap.indent(
            json.dumps(
                fgr.core.utils.parse_incoming_log_message(msg, level),
                default=fgr.core.utils.convert_for_representation,
                indent=Constants.INDENT,
                sort_keys=True
                ) + '\n',
            Constants.INDENT * ' '
            )
        with self.assertLogs(self.log, level) as logger:
            fgr.log.error(msg)
            self.assertEqual(logger.records[0].msg, expected_output)

    def test_05_log(self):
        """Test exc logging."""

        msg = self.msg_str
        level = fgr.log.logging.ERROR
        parsed = fgr.core.utils.parse_incoming_log_message(msg, level)
        with self.assertLogs(self.log, level) as logger:
            try:
                _ = 1 / 0
            except Exception:
                fgr.log.error(msg)
                parsed['traceback'] = traceback.format_exc()
                expected_output = textwrap.indent(
                    json.dumps(
                        parsed,
                        default=fgr.core.utils.convert_for_representation,
                        indent=Constants.INDENT,
                        sort_keys=True
                        ) + '\n',
                    Constants.INDENT * ' '
                    )
            self.assertEqual(logger.records[0].msg, expected_output)

    def test_06_log(self):
        """Test exc logging."""

        msg = self.msg_str
        level = fgr.log.logging.DEBUG
        parsed = fgr.core.utils.parse_incoming_log_message(msg, level)
        with self.assertLogs(self.log, level) as logger:
            try:
                _ = 1 / 0
            except Exception as e:
                self.log.debug(msg, exc_info=e)
                parsed['traceback'] = traceback.format_exc()
                expected_output = textwrap.indent(
                    json.dumps(
                        parsed,
                        default=fgr.core.utils.convert_for_representation,
                        indent=Constants.INDENT,
                        sort_keys=True
                        ) + '\n',
                    Constants.INDENT * ' '
                    )
            self.assertEqual(logger.records[0].msg, expected_output)

    def test_07_print(self):
        """Test first print + warning interception."""

        msg = self.msg_str
        level = fgr.log.logging.WARNING
        parsed = fgr.core.utils.parse_incoming_log_message(
            Constants.WARN_MSG,
            level
            )
        with self.assertLogs(self.log, level) as logger:
            print(msg)
            expected_output = textwrap.indent(
                json.dumps(
                    parsed,
                    default=fgr.core.utils.convert_for_representation,
                    indent=Constants.INDENT,
                    sort_keys=True
                    ) + '\n',
                Constants.INDENT * ' '
                )
            self.assertEqual(
                logger.records[0].msg,
                expected_output
                )

    def test_08_print(self):
        """Test subsequent print interceptions."""

        msg = self.msg_str
        with self.assertWarns(Warning) as emitter:
            with self.assertNoLogs(self.log):
                print(msg)
                self.assertEqual(
                    emitter.warnings[0].message.args[0],
                    Constants.WARN_MSG
                    )


class TestDeployedLogger(unittest.TestCase):
    """Fixture for testing logger in higher environments."""

    def setUp(self) -> None:
        fgr.log._log.cache_clear()
        fgr.core.constants.PackageConstants.ENV = 'dev'
        self.log = fgr.log._log()
        self.msg = mocking.examples.Pet
        return super().setUp()

    def test_01_print(self):
        """Test first print + warning interception."""

        msg = self.msg
        warn_msg = '\n'.join(
            (
                '.py:line_no: WarningClass: ',
                Constants.SILENCE_MSG,
                str(msg),
                'warnings.warn()'
                )
            )
        level = fgr.log.logging.WARNING
        parsed = fgr.core.utils.parse_incoming_log_message(warn_msg, level)
        with self.assertLogs(self.log, level) as logger:
            print(msg)
            expected_output = textwrap.indent(
                json.dumps(
                    parsed,
                    default=fgr.core.utils.convert_for_representation,
                    indent=Constants.INDENT,
                    sort_keys=True
                    ) + '\n',
                Constants.INDENT * ' '
                )
            self.assertEqual(
                logger.records[0].msg,
                expected_output
                )

    def test_02_print(self):
        """Test subsequent, same message print interceptions."""

        msg = self.msg
        warn_msg = '\n'.join(
            (
                Constants.SILENCE_MSG,
                str(msg),
                )
            )
        with self.assertWarns(Warning) as emitter:
            with self.assertNoLogs(self.log):
                print(msg)
                self.assertEqual(
                    emitter.warnings[0].message.args[0],
                    warn_msg
                    )

    def test_03_print(self):
        """Test subsequent, new message print + warning interception."""

        msg = 'testing'
        warn_msg = '\n'.join(
            (
                '.py:line_no: WarningClass: ',
                Constants.SILENCE_MSG,
                str(msg),
                'warnings.warn()'
                )
            )
        level = fgr.log.logging.WARNING
        parsed = fgr.core.utils.parse_incoming_log_message(warn_msg, level)
        with self.assertLogs(self.log, level) as logger:
            print(msg)
            expected_output = textwrap.indent(
                json.dumps(
                    parsed,
                    default=fgr.core.utils.convert_for_representation,
                    indent=Constants.INDENT,
                    sort_keys=True
                    ) + '\n',
                Constants.INDENT * ' '
                )
            self.assertEqual(
                logger.records[0].msg,
                expected_output
                )

    def test_04_ext_warning(self):
        """Test external warning interception."""

        msg = repr(self.msg)
        level = fgr.log.logging.WARNING
        parsed = fgr.core.utils.parse_incoming_log_message(msg, level)
        with self.assertLogs(self.log, level) as logger:
            warnings.warn(msg, stacklevel=1)
            expected_output = textwrap.indent(
                json.dumps(
                    parsed,
                    default=fgr.core.utils.convert_for_representation,
                    indent=Constants.INDENT,
                    sort_keys=True
                    ) + '\n',
                Constants.INDENT * ' '
                )
            self.assertEqual(
                logger.records[0].msg,
                expected_output
                )

    def test_05_invalid_log_type_exc(self):
        """Test correct exc is raised."""

        with self.assertNoLogs(self.log):
            self.assertRaises(
                fgr.core.exceptions.InvalidLogMessageTypeError,
                lambda: fgr.log.info(list())
                )

    def test_06_log_truncation(self):
        """Test long strings correctly truncated."""

        msg = {'longString': 'ABCDEFG' * 1024}
        level = fgr.log.logging.CRITICAL
        with self.assertLogs(self.log, level) as logger:
            fgr.log.critical(msg)
            self.assertIn(
                Constants.M_LINE_TOKEN,
                logger.records[0].msg
                )

    def test_07_log_redaction(self):
        """Test sensitive strings correctly redacted."""

        msg = {'apiKey': 'ABCDEFG'}
        level = fgr.log.logging.INFO
        with self.assertLogs(self.log, level) as logger:
            fgr.log.info(msg)
            self.assertIn(
                '[ REDACTED :: API KEY ]',
                logger.records[0].msg
                )

    def tearDown(self) -> None:
        fgr.log._log.cache_clear()
        fgr.core.constants.PackageConstants.ENV = 'local'
        return super().tearDown()
