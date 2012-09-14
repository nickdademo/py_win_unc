from unittest import main, TestCase

from win_unc.internal.net_use_table import parse_net_use_table


EMPTY_TABLE = '''
There are no entries in the list.
'''

VALID_TABLE = '''
New connections will be remembered.


Status       Local     Remote                    Network

-------------------------------------------------------------------------------
OK           A:        \\\\some.remote.path\\with-a-long-path
                                                Microsoft Windows Network
Disconnected B:        \\\\localhost               Microsoft Windows Network
OK           C:        \\\\localhost\\has    spaces Microsoft Windows Network
Unavailable  D:        \\\\
            Microsoft Windows Network
The command completed successfully.

'''


class TestGetMountedUncPaths(TestCase):
    def assertEqualSets(self, a, b):
        """
        Asserts that containers `a` and `b` are equal disregarding ordering.
        """
        self.assertEqual(set(a), set(b))
        self.assertEqual(len(a), len(b))

    def test_empty_table(self):
        table = parse_net_use_table(EMPTY_TABLE)
        self.assertEqual(table.get_mounted_paths(), [])
        self.assertEqual(table.get_mounted_drives(), [])

    def test_valid_table(self):
        table = parse_net_use_table(VALID_TABLE)

        mounted_paths = ['\\\\',
                         '\\\\localhost',
                         '\\\\localhost\\has    spaces',
                         '\\\\some.remote.path\\with-a-long-path']
        self.assertEqualSets(table.get_mounted_paths(), mounted_paths)

        mounted_drives = ['A:', 'B:', 'C:', 'D:']
        self.assertEqualSets(table.get_mounted_drives(), mounted_drives)


if __name__ == '__main__':
    main()
