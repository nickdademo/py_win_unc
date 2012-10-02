from unittest import TestCase

from win_unc.errors import ShellCommandError
from win_unc.internal.shell import run


class TestShell(TestCase):
    def test_valid(self):
        self.assertIsNotNone(run('dir'))

    def test_error(self):
        self.assertRaises(ShellCommandError, run, '!')
