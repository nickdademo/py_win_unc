import os
import string

from stringlike import StringLike

from win_unc.errors import NoDrivesAvailableError, InvalidDiskDriveError
from win_unc.validators import is_valid_drive_letter


class DiskDrive(StringLike):
    def __init__(self, drive):
        """
        Creates a `DiskDrive` from a `drive_letter`.
        `drive` may be a string-like object or a `DiskDrive`-like object.
            * If it is a string-like object, then it must be the path to a Windows disk drive
              (from 'A:' to 'Z:', case-insensitive).
            * If it is a `DiskDrive`-like object, then this will clone it by returning a new
              `DiskDrive` with the same path.
        """
        letter = drive.drive_letter if hasattr(drive, 'drive_letter') else drive
        letter = letter.upper().rstrip(':\\')

        if not is_valid_drive_letter(letter):
            raise InvalidDiskDriveError(drive)
        else:
            self.drive_letter = letter + ':'


    def __str__(self):
        """
        Returns the `DiskDrive`'s drive letter. This is used by the `StringLike` parent class to
        mimic Python strings.
        """
        return self.drive_letter

    def __repr__(self):
        return '<{cls}: {str}>'.format(cls=self.__class__.__name__, str=str(self))


def get_available_disk_drive():
    """
    Returns the first available Windows disk drive. The search starts with "Z" since the later
    letters are not as commonly mapped. If the system does not have any drive letters available
    this will raise a `NoDrivesAvailableError`.
    """
    for letter in reversed(string.ascii_uppercase):
        if not os.path.isdir(letter + ':\\'):
            return DiskDrive(letter)
    else:
        raise NoDrivesAvailableError()
