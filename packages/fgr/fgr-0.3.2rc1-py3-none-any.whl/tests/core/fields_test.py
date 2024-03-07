import json
import typing
import unittest

import fgr

from . import mocking


class TestField(unittest.TestCase):
    """Fixture for testing the object."""

    def setUp(self) -> None:
        self.int_field = fgr.Field(
            name='int_field',
            default=1,
            type=int,
            )
        self.str_field = fgr.Field(
            name='str_field',
            default='a',
            type=str,
            )
        self.union_field = fgr.Field(
            name='union_field',
            default='a',
            type=int | str,
            )
        self.blank_field = fgr.Field(
            name='str_field',
            type=str,
            )
        return super().setUp()

    def test_01_hash(self):
        """Test __hash__."""

        self.assertTrue(
            (
                self.str_field.__field_hash__()
                == (
                    fgr.core.modules.Modules.fields.Field(  # type: ignore[attr-defined]
                        **dict(self.str_field)
                        ).__field_hash__()
                    )
                == hash(
                    ''.join(
                        (
                            fgr.Field.__name__,
                            repr(self.str_field.type),
                            repr(self.str_field.default),
                            self.str_field.name
                            )
                        )
                    )
                ) and self.str_field != self.int_field
            )

    def test_02_validate_comparison_exc(self):
        """Test invalid comparison type error raised."""

        self.assertRaises(
            fgr.core.exceptions.InvalidComparisonTypeError,
            lambda: self.str_field % 2
            )

    def test_03_validate_comparison_container_exc(self):
        """Test invalid container comparison error raised."""

        self.assertRaises(
            fgr.core.exceptions.InvalidContainerComparisonTypeError,
            lambda: self.int_field % 2
            )

    def test_04_validate_comparison_union_exc(self):
        """Test invalid comparison type error raised for Unions."""

        self.assertRaises(
            fgr.core.exceptions.InvalidComparisonTypeError,
            lambda: self.union_field != True
            )

    def test_05_lshift_overwrite(self):
        """Test __lshift__ updates when passed type same as self."""

        interpolated = self.blank_field << self.str_field
        self.assertEqual(interpolated.default, self.str_field.default)

    def test_06_repr_overwrite(self):
        """Test __repr__ same as _fields.Field."""

        self.assertEqual(
            repr(mocking.Derivative.bool_field),
            repr(
                fgr.core.modules.Modules.fields.Field(  # type: ignore[attr-defined]
                    **dict(mocking.Derivative.bool_field)
                    )
                )
            )

    def test_07_field_set_type_error(self):
        """Test __setitem__ raises correct exc if Field has invalid type."""

        self.assertRaises(
            fgr.core.exceptions.IncorrectTypeError,
            lambda: fgr.core.meta.Meta.__setitem__(
                fgr.Field,
                'name',
                fgr.Field(
                    name='str_field',
                    default='value',
                    type=int,
                    )
                )
            )


class TestFieldValidation(unittest.TestCase):
    """Fixture for testing the object."""

    def setUp(self) -> None:
        self.cls = mocking.TripDeriv
        return super().setUp()

    def test_01_parse_dtype(self):
        """Test correct exc raised if not nullable."""

        self.assertRaises(
            fgr.core.exceptions.IncorrectTypeError,
            lambda: self.cls.non_nullable_field.parse_dtype(None)
            )

    def test_02_parse_dtype(self):
        """Test None."""

        self.assertIsNone(self.cls.required_field.parse_dtype(None))

    def test_03_parse_dtype(self):
        """Test bool."""

        self.assertIs(
            self.cls.bool_field.parse_dtype('true'),
            True
            )

    def test_04_parse_dtype(self):
        """Test decimal."""

        self.assertIsInstance(
            self.cls.decimal_field.parse_dtype('4.5'),
            self.cls.decimal_field.type
            )

    def test_05_parse_dtype(self):
        """Test str null."""

        self.assertIsNone(self.cls.null_field.parse_dtype('null'))

    def test_06_parse_dtype(self):
        """Test unknown str exc."""

        self.assertRaises(
            fgr.core.exceptions.IncorrectTypeError,
            lambda: self.cls.null_field.parse_dtype('asdf')
            )

    def test_07_parse_dtype(self):
        """Test Object from dict."""

        self.assertIsInstance(
            self.cls.new_deriv.parse_dtype(dict(self.cls.new_deriv.default)),
            self.cls.new_deriv.type
            )

    def test_08_parse_dtype(self):
        """Test Union."""

        self.assertIsInstance(
            self.cls.forward_ref_union_field.parse_dtype('testing'),
            typing.get_args(self.cls.forward_ref_union_field.type)
            )

    def test_09_parse_dtype(self):
        """Test Union."""

        self.assertRaises(
            fgr.core.exceptions.IncorrectTypeError,
            lambda: self.cls.forward_ref_union_field.parse_dtype(False),
            )

    def test_10_parse_dtype(self):
        """Test Object from json."""

        self.assertIsInstance(
            self.cls.new_deriv.parse_dtype(repr(self.cls.new_deriv.default)),
            self.cls.new_deriv.type
            )

    def test_11_parse_dtype(self):
        """Test any dict."""

        self.assertEqual(
            self.cls.dict_field.parse_dtype(
                json.dumps(
                    self.cls.generic_dict_field.default
                    )
                ),
            self.cls.generic_dict_field.default
            )

    def test_12_parse_dtype(self):
        """Test generic dict."""

        self.assertRaises(
            fgr.core.exceptions.IncorrectTypeError,
            lambda: self.cls.generic_dict_field.parse_dtype(
                json.dumps(self.cls.dict_field.default)
                ),
            )

    def test_13_parse_dtype(self):
        """Test any array."""

        self.assertEqual(
            self.cls.tuple_field.parse_dtype(
                json.dumps(
                    self.cls.generic_tuple_field.default
                    )
                ),
            self.cls.generic_tuple_field.default
            )

    def test_14_parse_dtype(self):
        """Test generic array."""

        self.assertRaises(
            fgr.core.exceptions.IncorrectTypeError,
            lambda: self.cls.generic_tuple_field.parse_dtype(
                json.dumps(self.cls.tuple_field.default)
                ),
            )
