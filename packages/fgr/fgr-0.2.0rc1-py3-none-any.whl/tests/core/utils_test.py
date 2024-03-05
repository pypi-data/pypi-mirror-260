import unittest

import fgr

from . import mocking


class TestUtils(unittest.TestCase):
    """Fixture for testing utility functions."""

    def setUp(self) -> None:
        self.camelCaseString1 = 'caseString1'
        self.camelCaseString2 = 'caseStringCAPPED'
        self.camelCaseString3 = 'caseStringCAPPED123'
        self.camelCaseString5 = 'caseStringCAPPEDWithID'
        self.camelCaseString6 = 'caseStringCAPPEDWithId'
        self.snake_case_string_1 = 'case_string_1'
        self.snake_case_string_2 = 'case_string_CAPPED'
        self.snake_case_string_3 = 'case_string_CAPPED123'
        self.snake_case_string_4 = 'case_string_CAPPED_123'
        self.snake_case_string_5 = 'case_string_CAPPED_with_ID'
        self.snake_case_string_6 = 'case_string_CAPPED_with_id'
        self.kebab_case_string_1 = 'case-string-1'
        return super().setUp()

    def test_01_casing(self):
        """Test utils casing functions."""

        self.assertEqual(
            fgr.core.utils.camel_case_to_snake_case(self.camelCaseString1),
            self.snake_case_string_1
            )

    def test_02_casing(self):
        """Test utils casing functions."""

        self.assertEqual(
            fgr.core.utils.camel_case_to_snake_case(self.camelCaseString2),
            self.snake_case_string_2
            )

    def test_03_casing(self):
        """Test utils casing functions."""

        self.assertEqual(
            fgr.core.utils.camel_case_to_snake_case(self.camelCaseString3),
            self.snake_case_string_3
            )

    def test_04_casing(self):
        """Test utils casing functions."""

        self.assertEqual(
            fgr.core.utils.to_camel_case(self.snake_case_string_1),
            self.camelCaseString1
            )

    def test_05_casing(self):
        """Test utils casing functions."""

        self.assertEqual(
            fgr.core.utils.to_camel_case(self.snake_case_string_2),
            self.camelCaseString2
            )

    def test_06_casing(self):
        """Test utils casing functions."""

        self.assertEqual(
            fgr.core.utils.to_camel_case(self.snake_case_string_3),
            self.camelCaseString3
            )

    def test_07_casing(self):
        """Test utils casing functions."""

        self.assertEqual(
            fgr.core.utils.to_camel_case(self.snake_case_string_4),
            self.camelCaseString3
            )

    def test_08_casing(self):
        """Test utils casing functions."""

        self.assertNotEqual(
            fgr.core.utils.camel_case_to_snake_case(self.camelCaseString3),
            self.snake_case_string_4
            )

    def test_09_casing(self):
        """Test utils casing functions."""

        self.assertEqual(
            fgr.core.utils.camel_case_to_kebab_case(self.camelCaseString1),
            self.kebab_case_string_1
            )

    def test_10_casing(self):
        """Test utils casing functions."""

        self.assertEqual(
            fgr.core.utils.camel_case_to_snake_case(self.camelCaseString5),
            self.snake_case_string_5
            )

    def test_11_casing(self):
        """Test utils casing functions."""

        self.assertEqual(
            fgr.core.utils.to_camel_case(self.snake_case_string_5),
            self.camelCaseString5
            )

    def test_12_casing(self):
        """Test utils casing functions."""

        self.assertEqual(
            fgr.core.utils.camel_case_to_snake_case(self.camelCaseString6),
            self.snake_case_string_6
            )

    def test_13_casing(self):
        """Test utils casing functions."""

        self.assertEqual(
            fgr.core.utils.to_camel_case(self.snake_case_string_6),
            self.camelCaseString6
            )

    def test_14_key_for_non_string(self):
        """Test utils key_for functions."""

        self.assertIsNone(fgr.core.utils.key_for(mocking.DubDeriv, 24))
