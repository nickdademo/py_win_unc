from unittest import TestCase

from win_unc.internal.shell import run
from win_unc.unc_directory import UncDirectory
from win_unc.internal.current_state import get_current_net_use_table


LOCALHOST_UNC = r'\\localhost\IPC$'


class LocalHostConnectionTest(TestCase):
    def setUp(self):
        self.localhost_was_connected = self.localhost_is_connected()

    def tearDown(self):
        if self.localhost_was_connected:
            self.disconnect_localhost()

    def connect_localhost(self):
        if not self.localhost_is_connected():
            run('NET USE ' + LOCALHOST_UNC)

    def disconnect_localhost(self):
        if self.localhost_is_connected():
            run('NET USE ' + LOCALHOST_UNC + ' /DELETE')

    def localhost_is_connected(self):
        net_use = get_current_net_use_table()
        return UncDirectory(LOCALHOST_UNC) in net_use.get_connected_paths()
