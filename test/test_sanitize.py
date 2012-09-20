from unittest import TestCase

from win_unc.internal.sanitize import sanitize_for_shell, sanitize_logon, sanitize_path


class TestSanitize(TestCase):
    def test_sanitize_for_shell(self):
        self.assertEqual(sanitize_for_shell(''), '')
        self.assertEqual(sanitize_for_shell('"'), r'\"')
        self.assertEqual(sanitize_for_shell('abc'), 'abc')
        self.assertEqual(sanitize_for_shell('abc"""'), r'abc\"\"\"')

    def test_sanitize_for_logon(self):
        self.assertEqual(sanitize_logon(''), '')

    def test_sanitize_path(self):
        self.assertEqual(sanitize_path(''), '')
        self.assertEqual(sanitize_path(r'C:\a valid\folder'), r'C:\a valid\folder')
        self.assertEqual(sanitize_path(r':\\'), r':\\')
        self.assertEqual(sanitize_path(r'<>"/|?*'), '')
        self.assertEqual(sanitize_path('\0\1\2\3\4\30\31'), '')
