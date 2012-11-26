from unittest import TestCase

from win_unc.internal.shell import run
from win_unc.unc_directory import UncDirectory
from win_unc.internal.current_state import get_current_net_use_table


LOCALHOST_UNC = r'\\localhost\IPC$'


class LocalHostConnectionTest(TestCase):
    def connect_localhost(self):
        self.localhost_was_connected = self.localhost_connected()
        if self.localhost_was_connected:
            run('NET USE ' + LOCALHOST_UNC + ' /DELETE')

    def disconnect_localhost(self):
        if self.localhost_was_connected:
            run('NET USE ' + LOCALHOST_UNC)

    def localhost_connected(self):
        net_use = get_current_net_use_table()
        return UncDirectory(LOCALHOST_UNC) in net_use.get_connected_paths()
