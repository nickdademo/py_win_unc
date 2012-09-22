from unittest import TestCase

from win_unc.connecting import UncDirectory


class TestUncDirectory(TestCase):
    def test_eqality_operators(self):
        self.assertEqual(UncDirectory('path'), UncDirectory('path'))
        self.assertEqual(UncDirectory('path'), UncDirectory('PATH'))

        self.assertEqual(UncDirectory('path', 'username'), UncDirectory('path', 'username'))
        self.assertEqual(UncDirectory('path', 'username'), UncDirectory('PATH', 'username'))
        self.assertNotEqual(UncDirectory('path', 'username'), UncDirectory('path', 'USERNAME'))

        self.assertEqual(UncDirectory('path', 'username', 'password'),
                         UncDirectory('path', 'username', 'password'))
        self.assertEqual(UncDirectory('path', 'username', 'password'),
                         UncDirectory('PATH', 'username', 'password'))
        self.assertNotEqual(UncDirectory('path', 'username', 'password'),
                            UncDirectory('path', 'username', 'PASSWORD'))

        self.assertNotEqual(UncDirectory('path'), None)
        self.assertNotEqual(UncDirectory('path'), 'somestring')
