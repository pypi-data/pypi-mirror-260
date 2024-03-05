import unittest

import fgr


class TestDtypes(unittest.TestCase):
    """Fixture for testing the object."""

    def setUp(self) -> None:
        self.int_field = fgr.Field[int]
        return super().setUp()

    def test_01_field_alias_repr(self):
        """Test __repr__ for Field alias."""

        self.assertEqual(
            repr(self.int_field),
            'Field[int]'
            )
