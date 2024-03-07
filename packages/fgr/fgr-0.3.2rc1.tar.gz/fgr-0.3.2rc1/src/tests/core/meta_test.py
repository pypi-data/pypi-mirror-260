import json
import typing
import unittest

import fgr

from . import mocking


class TestBase(unittest.TestCase):
    """Fixture for testing Base."""

    def setUp(self) -> None:
        self.mcs = fgr.core.meta.Meta
        self.cls = mocking.Derivative
        self.object_ = self.cls()
        self.trip = mocking.TripDeriv(
            str_field='123',
            )
        self.anti = mocking.AntiTripDeriv(
            str_field='321'
            )
        return super().setUp()

    def test_01_dict_functionality(self):
        """Test Base __getitem__."""

        self.assertTrue(
            self.object_['int_field']
            == self.object_.int_field
            == self.cls.int_field.default
            )

    def test_02_dict_functionality(self):
        """Test Base __getitem__ raises KeyError if no key."""

        self.assertRaises(
            KeyError,
            lambda: self.object_['field_that_does_not_exist']
            )

    def test_03_iter(self):
        """Test Base __iter__."""

        self.assertEqual(dict(self.object_.__iter__()), dict(self.object_))

    def test_04_len(self):
        """Test Base __len__."""

        self.assertEqual(len(self.object_), len(self.cls.__fields__))

    def test_05_contains(self):
        """Test Base __contains__."""

        self.assertIn(self.object_.fields[0], self.object_)

    def test_06_ne(self):
        """Test Base __ne__."""

        self.assertFalse(self.object_ != self.object_)

    def test_07_lshift(self):
        """Test Base __lshift__ correctly interpolates."""

        object_ = self.trip << self.anti
        self.assertNotEqual(object_.str_field, self.anti.str_field)

    def test_08_lshift(self):
        """Test Base __lshift__ correctly interpolates."""

        object_ = self.trip << self.anti
        self.assertNotEqual(object_.other_field, self.trip.other_field)

    def test_09_rshift(self):
        """Test Base __rshift__ correctly overwrites."""

        default = mocking.TripDeriv()
        object_ = self.trip >> default
        self.assertNotEqual(object_.str_field, default.str_field)

    def test_10_rshift(self):
        """Test Base __rshift__ correctly overwrites."""

        object_ = self.trip >> self.anti
        self.assertEqual(object_.str_field, self.anti.str_field)

    def test_11_dict_functionality(self):
        """Test Base get returns default if no key."""

        self.assertIsNone(self.object_.get('field_that_does_not_exist'))

    def test_12_to_dict(self):
        """Test Base to_dict."""

        self.assertDictEqual(
            {
                fgr.core.utils.to_camel_case(k): self.trip[k]
                for k, v in self.trip.items()
                if type(v) in typing.get_args(fgr.core.dtypes.Primitive)
                },
            {
                k: v
                for k, v
                in self.trip.to_dict(camel_case=True).items()
                if type(v) in typing.get_args(fgr.core.dtypes.Primitive)
                }
            )

    def test_13_to_dict(self):
        """Test Base to_dict."""

        self.assertDictEqual(
            {k: v for k, v in self.object_ if v is not None},
            self.object_.to_dict(include_null=False)
            )

    def test_14_repr(self):
        """Test Base __repr__."""

        self.assertEqual(
            repr(self.trip),
            json.dumps(
                dict(self.trip),
                default=fgr.core.utils.convert_for_representation,
                indent=fgr.core.constants.PackageConstants.INDENT,
                sort_keys=True
                )
            )


class TestMeta(unittest.TestCase):
    """Fixture for testing Meta."""

    def setUp(self) -> None:
        self.mcs = fgr.core.meta.Meta
        self.cls = mocking.Derivative
        self.field = fgr.Field(
            name='str_field',
            default='value',
            type=str,
            )
        return super().setUp()

    def test_01_dict_functionality(self):
        """Test Meta __getitem__."""

        self.assertIsInstance(
            self.cls['str_field'],
            fgr.Field
            )

    def test_02_dict_functionality(self):
        """Test Meta __getitem__ with type input returns Field alias."""

        self.assertIsInstance(
            fgr.Field[str],
            fgr.core.dtypes.Field
            )

    def test_03_dict_functionality(self):
        """Test Meta __getitem__ with type input raises KeyError if not Field."""

        self.assertRaises(KeyError, lambda: self.cls[str])

    def test_04_dict_functionality(self):
        """Test __setitem__ raises correct exc if value is not FieldType."""

        self.assertRaises(
            fgr.core.exceptions.IncorrectTypeError,
            lambda: self.mcs.__setitem__(self.cls, self.field.name, 'value')
            )

    def test_05_dict_functionality(self):
        """Test __setitem__ raises correct exc if Field with invalid name."""

        self.assertRaises(
            fgr.core.exceptions.InvalidFieldRedefinitionError,
            lambda: self.mcs.__setitem__(
                self.cls,
                self.field.name,
                fgr.Field(
                    name='_str_field',
                    default='value',
                    type=str,
                    )
                )
            )

    def test_06_dict_functionality(self):
        """Test __setitem__ raises correct exc if Field has invalid type."""

        self.assertRaises(
            fgr.core.exceptions.IncorrectTypeError,
            lambda: self.mcs.__setitem__(
                self.cls,
                self.field.name,
                fgr.Field(
                    name='str_field',
                    default='value',
                    type=int,
                    )
                )
            )

    def test_07_dict_functionality(self):
        """Test __setitem__ raises correct exc if Field does not exist."""

        self.assertRaises(
            fgr.core.exceptions.InvalidFieldRedefinitionError,
            lambda: self.mcs.__setitem__(
                self.cls,
                'field_that_does_not_exist',
                fgr.Field(
                    name='str_field',
                    default='value',
                    type=str,
                    )
                )
            )

    def test_08_repr_functionality(self):
        """Test __repr__ is nice."""

        self.assertEqual(
            repr(self.cls),
            json.dumps(
                fgr.core.utils.convert_for_representation(self.cls),
                default=fgr.core.utils.convert_for_representation,
                indent=fgr.core.constants.PackageConstants.INDENT,
                sort_keys=True
                )
            )

    def test_09_dict_keys(self):
        """Test keys."""

        self.assertListEqual(
            list(self.cls.keys()),
            list(self.cls.__fields__)
            )

    def test_10_dict_values(self):
        """Test values."""

        self.assertListEqual(
            list(self.mcs.values(self.cls)),
            list(self.cls.__fields__.values())
            )

    def test_11_dict_items(self):
        """Test items."""

        self.assertListEqual(
            list(self.mcs.items(self.cls)),
            list(self.cls.__fields__.items())
            )

    def test_12_dict_setitem(self):
        """Test __setitem__ actually works."""

        self.cls[self.field.name] = self.field
        self.assertEqual(
            self.cls()[self.field.name],
            self.field.default
            )

    def test_13_iter(self):
        """Test __iter__."""

        self.assertDictEqual(
            dict(self.mcs.__iter__(self.cls)),
            dict(self.cls)
            )

    def test_14_dict_get(self):
        """Test get."""

        self.assertEqual(
            self.mcs.get(self.cls, self.field.name),
            self.cls[self.field.name]
            )

    def test_15_dict_get_with_default(self):
        """Test get (default)."""

        self.assertIsNone(self.mcs.get(self.cls, 'not_a_field'))

    def test_15_dict_update(self):
        """Test update."""

        self.mcs.update(mocking.DubDeriv, mocking.MixinDeriv)
        self.assertEqual(
            mocking.DubDeriv.bob.default,
            mocking.MixinDeriv.bob.default
            )

    def test_16_dict_functionality(self):
        """Test __setitem__ raises correct exc if invalid default."""

        self.assertRaises(
            fgr.core.exceptions.IncorrectDefaultTypeError,
            lambda: self.mcs.__setitem__(
                self.cls,
                self.field.name,
                fgr.Field(
                    name='str_field',
                    default=4,
                    type=str,
                    )
                )
            )

    def test_17_classvar_skip(self):
        """Test ClassVar annotation skip."""

        self.mcs(
            'ExcTest',
            (fgr.core.meta.Base, ),
            {
                '__annotations__': {
                    self.field.name: typing.ClassVar[str],
                    },
                '__module__': self.__module__
                }
            )
        self.assertTrue(True)

    def test_18_finalvar_skip(self):
        """Test FinalVar annotation skip."""

        self.mcs(
            'ExcTest',
            (fgr.core.meta.Base, ),
            {
                '__annotations__': {
                    self.field.name: typing.Final[str],
                    },
                '__module__': self.__module__
                }
            )
        self.assertTrue(True)


class TestExceptions(unittest.TestCase):
    """Fixture for testing exceptions."""

    def setUp(self) -> None:
        self.mcs = fgr.core.meta.Meta
        self.field = fgr.Field(
            name='str_field',
            default='value',
            type=str,
            )
        return super().setUp()

    def test_01_no_reserved_fields(self):
        """Test cannot create with reserved keyword overwrites."""

        self.assertRaises(
            fgr.core.exceptions.ReservedKeywordError,
            lambda: self.mcs(
                'ExcTest',
                (fgr.core.meta.Base, ),
                {
                    '__cache__': {},
                    '__module__': self.__module__
                    }
                ),
            )

    def test_02_no_annotations(self):
        """Test cannot create without annotations."""

        self.assertRaises(
            fgr.core.exceptions.MissingTypeAnnotation,
            lambda: self.mcs(
                'ExcTest',
                (fgr.core.meta.Base, ),
                {
                    self.field.name: self.field,
                    '__annotations__': {},
                    '__module__': self.__module__
                    }
                ),
            )

    def test_03_non_field_annotations(self):
        """Test cannot create without FieldType annotations."""

        self.assertRaises(
            fgr.core.exceptions.FieldAnnotationeError,
            lambda: self.mcs(
                'ExcTest',
                (fgr.core.meta.Base, ),
                {
                    self.field.name: self.field,
                    '__annotations__': {
                        self.field.name: str,
                        },
                    '__module__': self.__module__
                    }
                ),
            )

    def test_04_no_reserved_annotations(self):
        """Test cannot create with reserved keyword overwrites."""

        self.assertRaises(
            fgr.core.exceptions.ReservedKeywordError,
            lambda: self.mcs(
                'ExcTest',
                (fgr.core.meta.Base, ),
                {
                    '__annotations__': {
                        '__cache__': {},
                        },
                    '__module__': self.__module__
                    }
                ),
            )

    def test_05_non_field_annotations(self):
        """Test cannot create without FieldType annotations."""

        self.assertRaises(
            fgr.core.exceptions.FieldAnnotationeError,
            lambda: self.mcs(
                'ExcTest',
                (fgr.core.meta.Base, ),
                {
                    '__annotations__': {
                        self.field.name: str,
                        },
                    '__module__': self.__module__
                    }
                ),
            )

    def test_06_inconsistent_casing(self):
        """Test cannot create with inconsistent field casing."""

        self.assertRaises(
            fgr.core.exceptions.IncorrectCasingError,
            lambda: self.mcs(
                'ExcTest',
                (fgr.core.meta.Base, ),
                {
                    '__annotations__': {
                        'string_field': fgr.Field[str],
                        'stringField': fgr.Field[str],
                        },
                    '__module__': self.__module__
                    }
                ),
            )
