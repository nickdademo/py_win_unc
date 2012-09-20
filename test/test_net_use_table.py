from unittest import TestCase

from win_unc.internal.net_use_table import NetUseTable, parse_net_use_table


EMPTY_TABLE = '''
There are no entries in the list.
'''

VALID_TABLE = r'''
New connections will be remembered.


Status       Local     Remote                    Network

-------------------------------------------------------------------------------
OK           A:        \\some.remote.path\with-a-long-path
                                                 Microsoft Windows Network
Disconnected B:        \\localhost               Microsoft Windows Network
OK           C:        \\localhost\has    spaces Microsoft Windows Network
Unavailable  D:        \\
            Microsoft Windows Network
OK                     \\localhost\IPC$          Microsoft Windows Network
The command completed successfully.

'''


class TestParsingNetUseTable(TestCase):
    """
    Tests correct parsing of the output from `NET USE`.
    """

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
                         '\\\\localhost\\IPC$',
                         '\\\\localhost\\has    spaces',
                         '\\\\some.remote.path\\with-a-long-path']
        self.assertEqualSets(table.get_mounted_paths(), mounted_paths)

        mounted_drives = ['A:', 'B:', 'C:', 'D:', '']
        self.assertEqualSets(table.get_mounted_drives(), mounted_drives)


def make_row(local='local', remote='remote', status='status'):
    return {'local': local, 'remote': remote, 'status': status}


class TestNetUseTable(TestCase):
    """
    Tests methods of the `NetUseTable` class.
    """

    def test_get_mounted_paths(self):
        table = NetUseTable()
        self.assertEqual(table.get_mounted_paths(), [])

        table.add_row(make_row(remote='remote1'))
        self.assertEqual(table.get_mounted_paths(), ['remote1'])
        
        table.add_row(make_row(remote='remote2'))
        self.assertEqual(table.get_mounted_paths(), ['remote1', 'remote2'])

    def test_get_mounted_drives(self):
        table = NetUseTable()
        self.assertEqual(table.get_mounted_drives(), [])

        table.add_row(make_row(local='local1'))
        self.assertEqual(table.get_mounted_drives(), ['local1'])
        
        table.add_row(make_row(local='local2'))
        self.assertEqual(table.get_mounted_drives(), ['local1', 'local2'])

    def test_get_matching_rows(self):
        table = NetUseTable()
        
        self.assertEqual(table.get_matching_rows({}), [])
        self.assertEqual(table.get_matching_rows({'local': 'local'}), [])
        
        row1 = make_row(local='local1', remote='remote1')
        row2 = make_row(local='local2', remote='remote2')
        row3 = make_row(local='local3', remote='remote2')
        table.add_row(row1)
        table.add_row(row2)
        table.add_row(row3)

        self.assertEqual(table.get_matching_rows({'bad': 'bad'}), [])
        self.assertEqual(table.get_matching_rows({}), [row1, row2, row3])
        self.assertEqual(table.get_matching_rows({'local': 'local3'}), [row3])
        self.assertEqual(table.get_matching_rows({'remote': 'remote2'}), [row2, row3])
        self.assertEqual(table.get_matching_rows({'status': 'status'}), [row1, row2, row3])

        self.assertEqual(table.get_matching_rows({'remote': 'remote2', 'status': 'status'}),
                         [row2, row3])
        self.assertEqual(table.get_matching_rows({'status': 'status', 'bad': 'bad'}), [])
