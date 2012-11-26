import win_unc.query as Q
from win_unc.unc_directory import UncDirectory

from connection_test_utils import LocalHostConnectionTest


class TestGetCurrentConnections(LocalHostConnectionTest):
    def test_get_any(self):
        Q.get_current_connections()

    def test_add_localhost(self):
        if not self.localhost_is_connected():
            before = Q.get_current_connections()
            self.connect_localhost()
            after = Q.get_current_connections()
            self.assertEqual(len(before) + 1, len(after))

    def test_remove_localhost(self):
        if self.localhost_is_connected():
            before = Q.get_current_connections()
            self.disconnect_localhost()
            after = Q.get_current_connections()
            self.assertEqual(len(before) - 1, len(after))


class TestGetConnectionForUncDirectory(LocalHostConnectionTest):
    def test_no_match(self):
        self.disconnect_localhost()
        localhost = UncDirectory(r'\\localhost')
        self.assertIsNone(Q.get_connection_for_unc_directory(localhost))

    def test_match(self):
        self.connect_localhost()
        localhost = UncDirectory(r'\\localhost')
        self.assertEqual(Q.get_connection_for_unc_directory(localhost).unc, localhost)
