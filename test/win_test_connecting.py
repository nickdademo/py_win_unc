from win_unc.connecting import UncDirectoryConnection
from win_unc.unc_directory import UncDirectory

from connection_test_utils import LocalHostConnectionTest


class TestUncDirectoryConnection(LocalHostConnectionTest):
    def test_connect(self):
        unc = UncDirectory(r'\\localhost')
        conn = UncDirectoryConnection(unc)
        conn.connect()

        self.assertTrue(self.localhost_is_connected())
        self.assertTrue(conn.is_connected())

        conn.disconnect()

        self.assertFalse(self.localhost_is_connected())
        self.assertFalse(conn.is_connected())
