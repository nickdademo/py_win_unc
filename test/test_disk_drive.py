from unittest import TestCase

from win_unc.errors import InvalidDiskDriveError
from win_unc.disk_drive import DiskDrive


class TestDiskDrive(TestCase):
    def test_init_with_valid_string(self):
        self.assertEqual(DiskDrive('A:').drive_letter, 'A:')
        self.assertEqual(DiskDrive('a:').drive_letter, 'A:')
        self.assertEqual(DiskDrive('a').drive_letter, 'A:')
        self.assertEqual(DiskDrive('A:\\').drive_letter, 'A:')
        self.assertEqual(DiskDrive('a:\\').drive_letter, 'A:')
        self.assertEqual(DiskDrive('Z:').drive_letter, 'Z:')

    def test_init_with_invalid_string(self):
        self.assertRaises(InvalidDiskDriveError, DiskDrive, '')
        self.assertRaises(InvalidDiskDriveError, DiskDrive, 'AA:')
        self.assertRaises(InvalidDiskDriveError, DiskDrive, ':')
        self.assertRaises(InvalidDiskDriveError, DiskDrive, '1')
        self.assertRaises(InvalidDiskDriveError, DiskDrive, '-')
        self.assertRaises(InvalidDiskDriveError, DiskDrive, 'abc')

    def test_init_for_clone(self):
        self.assertEqual(DiskDrive(DiskDrive('A:')).drive_letter, 'A:')
        self.assertEqual(DiskDrive(DiskDrive('Z:')).drive_letter, 'Z:')

    def test_str(self):
        self.assertEqual(str(DiskDrive('A:')), 'A:')

    def test_eq(self):
        self.assertEqual(DiskDrive('A:'), DiskDrive('A:'))
        self.assertNotEqual(DiskDrive('A:'), DiskDrive('Z:'))

    def test_stringlike(self):
        self.assertEqual(DiskDrive('A:'), 'A:')
        self.assertNotEqual(DiskDrive('A:'), 'Z:')
        self.assertEqual('A:', DiskDrive('A:'))
        self.assertNotEqual('A:', DiskDrive('Z:'))
