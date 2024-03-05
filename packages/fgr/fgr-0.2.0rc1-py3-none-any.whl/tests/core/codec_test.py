import datetime
import decimal
import unittest

import fgr


class TestCodec(unittest.TestCase):
    """Fixture for testing the object."""

    def setUp(self) -> None:
        self.datetime = datetime.datetime.now()
        self.decimal_float = decimal.Decimal(0.1)
        self.decimal_int = decimal.Decimal(10)
        return super().setUp()

    def test_01_datetime(self):
        """Test datetime to isoformat."""

        self.assertEqual(
            fgr.core.codec.encode(self.datetime),
            self.datetime.isoformat()
            )

    def test_02_decimal_float(self):
        """Test decimal to float."""

        self.assertEqual(
            fgr.core.codec.encode(self.decimal_float),
            float(self.decimal_float)
            )

    def test_03_decimal_int(self):
        """Test decimal to int."""

        self.assertEqual(
            fgr.core.codec.encode(self.decimal_int),
            int(self.decimal_int)
            )
