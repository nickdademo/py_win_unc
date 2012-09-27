from unittest import TestCase

from win_unc.connecting import get_current_net_use_table, UncDirectoryConnection
from win_unc.unc_directory import UncDirectory
from win_unc.internal.shell import run


LOCALHOST_UNC = r'\\localhost\IPC$'


class TestUncDirectoryConnection(TestCase):
    def setUp(self):
        self.localhost_was_connected = self.localhost_connected()
        if self.localhost_was_connected:
            run('NET USE ' + LOCALHOST_UNC + ' /DELETE')

    def tearDown(self):
        if self.localhost_was_connected:
            run('NET USE ' + LOCALHOST_UNC)

    def test_connect(self):
        unc = UncDirectory(r'\\localhost')
        conn = UncDirectoryConnection(unc)
        conn.connect()

        self.assertTrue(self.localhost_connected())
        self.assertTrue(conn.is_connected())

        conn.disconnect()

        self.assertFalse(self.localhost_connected())
        self.assertFalse(conn.is_connected())

    def localhost_connected(self):
        net_use = get_current_net_use_table()
        paths = [path.lower() for path in net_use.get_connected_paths()]
        return LOCALHOST_UNC.lower() in paths
