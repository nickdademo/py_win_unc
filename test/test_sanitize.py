from unittest import TestCase

from win_unc.internal import sanitize as lib


class TestSanitize(TestCase):
    def test_sanitize_for_shell(self):
        self.assertEqual(lib.sanitize_for_shell(''), '')
        self.assertEqual(lib.sanitize_for_shell('abcABC'), 'abcABC')
        self.assertEqual(lib.sanitize_for_shell('"'), r'\"')
        self.assertEqual(lib.sanitize_for_shell('abc"""'), r'abc\"\"\"')

    def test_sanitize_for_logon(self):
        self.assertEqual(lib.sanitize_logon(''), '')
        self.assertEqual(lib.sanitize_logon('abcABC'), 'abcABC')
        self.assertEqual(lib.sanitize_logon(r'"/[]:;|=,+*?<>'), '')
        self.assertEqual(lib.sanitize_logon(r'"/[]:;|=,+*?<>'), '')
        self.assertEqual(lib.sanitize_logon('\0'), '')

    def test_sanitize_path(self):
        self.assertEqual(lib.sanitize_path(''), '')
        self.assertEqual(lib.sanitize_path('abcABC'), 'abcABC')
        self.assertEqual(lib.sanitize_path(r'C:\a valid\folder'), r'C:\a valid\folder')
        self.assertEqual(lib.sanitize_path(r':\\'), r':\\')
        self.assertEqual(lib.sanitize_path(r'<>"/|?*'), '')
        self.assertEqual(lib.sanitize_path('\0\1\2\3\4\30\31'), '')

    def test_sanitize_file_name(self):
        self.assertEqual(lib.sanitize_file_name(''), '')
        self.assertEqual(lib.sanitize_file_name('abcABC'), 'abcABC')
        self.assertEqual(lib.sanitize_file_name(r'C:\a valid\folder'), r'Ca validfolder')
        self.assertEqual(lib.sanitize_file_name(r':\\'), r'')
        self.assertEqual(lib.sanitize_file_name(r'<>"/|?*'), '')
        self.assertEqual(lib.sanitize_file_name('\0\1\2\3\4\30\31'), '')
