import json
import unittest

import fgr
import fgr.core._fields


class TestPrivateField(unittest.TestCase):
    """Fixture for testing the object."""

    def setUp(self) -> None:
        self.owner = fgr.Field
        self.cls = fgr.core._fields.Field
        self.instance = self.cls(
            name='name',
            type=str,
            default=None,
            nullable=True,
            required=False,
            enum=None,
            )
        return super().setUp()

    def test_01_dunder_get_cls(self):
        """Test __get__ no instance."""

        self.assertEqual(
            self.owner.name,
            self.instance.__get__(None, self.owner)
            )

    def test_02_dunder_get_ins(self):
        """Test __get__ with instance."""

        self.assertEqual(
            self.instance.name,
            self.instance.__get__(
                self.owner(name=self.instance.name),
                self.owner
                )
            )

    def test_03_dunder_getattribute(self):
        """Test __getattribute__."""

        self.assertEqual(
            self.instance.name,
            self.instance['name']
            )

    def test_04_dunder_getattribute(self):
        """Test __getattribute__."""

        self.assertEqual(
            self.instance.__iter__,
            super(
                self.instance.__class__,
                self.instance
                ).__iter__
            )

    def test_05_dunder_repr(self):
        """Test __repr__."""

        self.assertEqual(
            self.instance['name'],
            json.loads(repr(self.instance))['name']
            )
