from unittest import TestCase

from win_unc import unc_directory as U
from win_unc.errors import InvalidUncPathError
from win_unc.unc_directory import UncDirectory, get_unc_directory_from_string
from win_unc.unc_credentials import UncCredentials


class TestUncDirectory(TestCase):
    def test_init_with_invalid_path(self):
        self.assertRaises(InvalidUncPathError, UncDirectory, '')
        self.assertRaises(InvalidUncPathError, UncDirectory, 'abc')
        self.assertRaises(InvalidUncPathError, UncDirectory, r'\\\abc')
        self.assertRaises(InvalidUncPathError, UncDirectory, r'C:\not-unc\path')

    def test_init_with_cloning(self):
        unc = UncDirectory(UncDirectory(r'\\path'))
        self.assertEqual(unc.get_path(), r'\\path')
        self.assertIsNone(UncDirectory(unc).get_username())
        self.assertIsNone(UncDirectory(unc).get_password())

        unc = UncDirectory(UncDirectory(r'\\path', 'user'))
        self.assertEqual(unc.get_path(), r'\\path')
        self.assertEqual(unc.get_username(), 'user')
        self.assertIsNone(unc.get_password())

        unc = UncDirectory(UncDirectory(r'\\path', None, 'pass'))
        self.assertEqual(unc.get_path(), r'\\path')
        self.assertIsNone(unc.get_username())
        self.assertEqual(unc.get_password(), 'pass')

        unc = UncDirectory(UncDirectory(r'\\path', 'user', 'pass'))
        self.assertEqual(unc.get_path(), r'\\path')
        self.assertEqual(unc.get_username(), 'user')
        self.assertEqual(unc.get_password(), 'pass')

    def test_eq(self):
        self.assertEqual(UncDirectory(r'\\path'), UncDirectory(r'\\path'))
        self.assertEqual(UncDirectory(r'\\path'), UncDirectory(r'\\PATH'))

        self.assertEqual(UncDirectory(r'\\path', 'user'), UncDirectory(r'\\path', 'user'))
        self.assertEqual(UncDirectory(r'\\path', 'user'), UncDirectory(r'\\PATH', 'user'))

        self.assertEqual(UncDirectory(r'\\path', 'user', 'pass'),
                         UncDirectory(r'\\path', 'user', 'pass'))
        self.assertEqual(UncDirectory(r'\\path', 'user', 'pass'),
                         UncDirectory(r'\\PATH', 'user', 'pass'))

    def test_ne(self):
        self.assertNotEqual(UncDirectory(r'\\path', 'user'), UncDirectory(r'\\path', 'USER'))
        self.assertNotEqual(UncDirectory(r'\\path', 'user', 'pass'),
                            UncDirectory(r'\\path', 'user', 'PASS'))
        self.assertIsNotNone(UncDirectory(r'\\path'))
        self.assertNotEqual(UncDirectory(r'\\path'), 'somestring')

    def test_get_normalized_path(self):
        self.assertEqual(UncDirectory(r'\\abc').get_normalized_path(), r'\\abc')
        self.assertEqual(UncDirectory(r'\\ABC').get_normalized_path(), r'\\abc')
        self.assertEqual(UncDirectory(r'\\abc\def').get_normalized_path(), r'\\abc\def')
        self.assertEqual(UncDirectory(r'\\abc\DEF').get_normalized_path(), r'\\abc\def')
        self.assertEqual(UncDirectory(r'\\abc\def\\').get_normalized_path(), r'\\abc\def')
        self.assertEqual(UncDirectory(r'\\abc\IPC$').get_normalized_path(), r'\\abc')
        self.assertEqual(UncDirectory(r'\\abc\ipc$').get_normalized_path(), r'\\abc')

    def test_str(self):
        self.assertEqual(str(UncDirectory(r'\\path')), r'\\path')
        self.assertEqual(str(UncDirectory(r'\\path', 'user')), r'user@\\path')
        self.assertEqual(str(UncDirectory(r'\\path', 'user', 'pass')), r'user:pass@\\path')

    def test_stringlike(self):
        self.assertEqual(UncDirectory(r'\\path'), r'\\path')
        self.assertEqual(r'\\path', UncDirectory(r'\\path'))


class TestParsing(TestCase):
    def test_get_unc_directory_from_string(self):
        self.assertEqual(get_unc_directory_from_string(r'\\path'), UncDirectory(r'\\path'))
        self.assertEqual(get_unc_directory_from_string(r'\\path\sub'),
                         UncDirectory(r'\\path\sub'))
        self.assertEqual(get_unc_directory_from_string(r'user@\\path'),
                         UncDirectory(r'\\path', 'user'))
        self.assertEqual(get_unc_directory_from_string(r':pass@\\path'),
                         UncDirectory(r'\\path', None, 'pass'))
        self.assertEqual(get_unc_directory_from_string(r'::@\\@\\path'),
                         UncDirectory(r'\\path', None, r':@\\'))
        self.assertEqual(get_unc_directory_from_string(r'user:pass@\\path'),
                         UncDirectory(r'\\path', 'user', 'pass'))
        self.assertEqual(get_unc_directory_from_string(r'user::@\\@\\path'),
                         UncDirectory(r'\\path', 'user', r':@\\'))
