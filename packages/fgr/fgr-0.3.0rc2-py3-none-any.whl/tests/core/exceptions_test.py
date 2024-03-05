import pickle
import unittest

import fgr


class TestExceptions(unittest.TestCase):
    """Fixture for testing exceptions."""

    def setUp(self) -> None:
        return super().setUp()

    def test_01_serialization(self):
        """Test multi-arg exc serializes correctly."""

        exc = fgr.core.exceptions.IncorrectCasingError(('a', 'b'))
        dump = pickle.dumps(exc)
        self.assertTupleEqual(
            exc.args,
            pickle.loads(dump).args
            )

    def test_02_serialization(self):
        """Test multi-arg exc serializes correctly."""

        exc = fgr.core.exceptions.IncorrectDefaultTypeError('test', str, 2)
        dump = pickle.dumps(exc)
        self.assertTupleEqual(
            exc.args,
            pickle.loads(dump).args
            )

    def test_03_serialization(self):
        """Test multi-arg exc serializes correctly."""

        exc = fgr.core.exceptions.IncorrectTypeError('test', str, 2)
        dump = pickle.dumps(exc)
        self.assertTupleEqual(
            exc.args,
            pickle.loads(dump).args
            )

    def test_04_serialization(self):
        """Test multi-arg exc serializes correctly."""

        exc = fgr.core.exceptions.InvalidComparisonTypeError('test', str, 2)
        dump = pickle.dumps(exc)
        self.assertTupleEqual(
            exc.args,
            pickle.loads(dump).args
            )

    def test_05_serialization(self):
        """Test multi-arg exc serializes correctly."""

        exc = fgr.core.exceptions.InvalidContainerComparisonTypeError(
            'test',
            list[str],
            2
            )
        dump = pickle.dumps(exc)
        self.assertTupleEqual(
            exc.args,
            pickle.loads(dump).args
            )

    def test_06_serialization(self):
        """Test exc serializes correctly."""

        exc = fgr.core.exceptions.InvalidLogMessageTypeError(42)
        dump = pickle.dumps(exc)
        self.assertTupleEqual(exc.args, pickle.loads(dump).args)

    def test_07_serialization(self):
        """Test exc serializes correctly."""

        exc = fgr.core.exceptions.FieldAnnotationeError('test', int)
        dump = pickle.dumps(exc)
        self.assertTupleEqual(exc.args, pickle.loads(dump).args)
