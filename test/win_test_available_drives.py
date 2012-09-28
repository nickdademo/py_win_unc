from unittest import TestCase

from win_unc.errors import NoDrivesAvailableError
from win_unc.disk_drive import get_available_disk_drive


class TestAvailableDiskDrive(TestCase):
    def test_get_available_disk_drive(self):
        try:
            self.assertIsNotNone(get_available_disk_drive())
        except NoDrivesAvailableError:
            pass
