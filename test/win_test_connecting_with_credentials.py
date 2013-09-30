from win_unc.connecting import UncDirectoryConnection
from win_unc.unc_directory import UncDirectory
from win_unc.unc_credentials import UncCredentials

from connection_test_utils import LocalHostConnectionTest


class TestUncDirectoryConnectionWithCredentials(LocalHostConnectionTest):
    """
    The purpose of this test is to check that the is_connected() method works correctly when using UncCredentials.
    """

    def mock_connect(self):
        """
        In the method test_connect(...), we cannot call conn.connect() as this creates an error.
        The error is that the command line 'NET USE ...' fails with the given credentials.

        The correct testing approach would be to use the mock-object pattern and provide a mock-command-runner.
        This avoids calling the command line.

        In the interest of minimum changes, a different appoach is taken here:
         > A mock connection is created that does not use credentials
         > The mock connection will be listed when calling "NET USE" 
         > The actual connenction's entry in "NET USE" would be exactly the same as the mock connection entry
         > The is_connected() method checks the state listed by "NET USE"
         > By using the mock connection, we can "fake" the return value of "NET USE" to be exactly what it would be if the actual connection had been connected successfully.  
        """
        mock_unc = UncDirectory(self.LOCALHOST_UNC)
        self.mock_conn = UncDirectoryConnection(mock_unc)
        self.mock_conn.connect()

    def mock_disconnect(self):
        self.mock_conn.disconnect()

    def test_connect(self):
        creds = UncCredentials('user', 'pass')
        unc = UncDirectory(self.LOCALHOST_UNC, creds)
        conn = UncDirectoryConnection(unc)
        self.mock_connect()

        self.assertTrue(self.localhost_is_connected())
        self.assertTrue(conn.is_connected())

        self.mock_disconnect()

        self.assertFalse(self.localhost_is_connected())
        self.assertFalse(conn.is_connected())
