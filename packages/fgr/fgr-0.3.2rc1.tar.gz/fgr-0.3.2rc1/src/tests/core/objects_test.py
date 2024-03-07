import unittest

import fgr

from . import mocking


class TestObject(unittest.TestCase):
    """Fixture for testing the object."""

    def setUp(self) -> None:
        self.cls = mocking.Derivative
        self.object_= self.cls(str_field='cba')
        return super().setUp()

    def test_01_dunder_get_cls(self):
        """Test fields.Field __get__."""

        self.assertIsInstance(
            self.cls.str_field,
            fgr.Field
            )

    def test_02_dunder_get_ins(self):
        """Test fields.Field __get__."""

        self.assertIsInstance(
            self.object_.str_field,
            self.cls.str_field.type
            )

    def test_03_casing(self):
        """Test casing."""

        self.assertTrue(self.cls.is_snake_case)

    def test_04_casing(self):
        """Test casing."""

        self.assertFalse(self.cls.isCamelCase)


class TestObjectDocumentationExamples(unittest.TestCase):
    """Test examples provided in Object __doc__."""

    def setUp(self) -> None:
        self.instance_values = {
            'id': 'abc123',
            '_alternate_id': 'dog1',
            'name': 'Bob',
            'type': 'dog',
            'in': 'timeout',
            'is_tail_wagging': False
            }
        self.new_name = 'Buddy'
        self.cls = mocking.examples.Pet
        self.object_= self.cls(
            id='abc123',
            _alternate_id='dog1',
            name='Bob',
            type='dog',
            in_='timeout',
            is_tail_wagging=False
            )
        self.object_from_dict = self.cls(self.instance_values)
        self.object_from_camel_case = self.cls(
            {
                'id': 'abc123',
                'alternateId': 'dog1',
                'name': 'Bob',
                'type': 'dog',
                'in': 'timeout',
                'isTailWagging': False
                }
            )
        return super().setUp()

    def test_01_instantiation(self):
        """Test __init__."""

        self.assertEqual(self.object_, self.object_from_dict)

    def test_02_instantiation_with_case_conversion(self):
        """Test __init__."""

        self.assertEqual(self.object_from_camel_case, self.object_)

    def test_03_dict_functionality(self):
        """Test __getitem__."""

        key = 'type'
        self.assertEqual(self.object_[key], self.instance_values[key])

    def test_04_dict_functionality(self):
        """Test __setitem__."""

        key = 'name'
        self.object_[key] = self.new_name
        self.assertTupleEqual(
            (self.new_name, self.new_name),
            (self.object_.name, self.object_[key])
            )

    def test_05_dict_functionality(self):
        """Test setdefault."""

        key = 'name'
        object_= self.cls()
        object_.setdefault(key, self.new_name)
        object_.setdefault(key, self.instance_values[key])
        self.assertTrue(
            getattr(object_, key)
            == self.new_name
            != self.instance_values[key]
            )

    def test_06_dict_keys(self):
        """Test keys."""

        self.assertListEqual(
            list(self.object_.keys()),
            list(self.instance_values)
            )

    def test_07_dict_values(self):
        """Test values."""

        self.assertListEqual(
            list(self.object_.values()),
            list(self.instance_values.values())
            )

    def test_08_dict_items(self):
        """Test items."""

        self.assertListEqual(
            list(self.object_.items()),
            list(self.instance_values.items())
            )

    def test_09_dict_key_error(self):
        """Test cannot set undefined field."""

        self.assertRaises(
            fgr.core.exceptions.InvalidFieldRedefinitionError,
            lambda: self.object_.__setitem__(
                'field_that_does_not_exist',
                self.new_name
                )
            )

    def test_10_dict_key_error(self):
        """Test cannot set undefined field."""

        self.assertRaises(
            fgr.core.exceptions.InvalidFieldRedefinitionError,
            lambda: self.object_.setdefault(
                'field_that_does_not_exist',
                self.new_name
                )
            )
