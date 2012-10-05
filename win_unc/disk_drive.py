import os
import string

from win_unc.cleaners import clean_drive_letter
from win_unc.errors import NoDrivesAvailableError, InvalidDiskDriveError
from win_unc.validators import is_valid_drive_letter


class DiskDrive(object):
    def __init__(self, drive):
        """
        Creates a `DiskDrive` from a `drive`.
        `drive` may be a string or a `DiskDrive`:
            * If it is a string, then it must be the path to a Windows disk drive
              (from 'A:' to 'Z:', case-insensitive).
            * If it is a `DiskDrive`, then this will clone it by returning a new `DiskDrive` with
              the same path.
        """
        new_letter = drive.drive_letter if isinstance(drive, self.__class__) else drive
        cleaned_letter = clean_drive_letter(new_letter)

        if is_valid_drive_letter(cleaned_letter):
            self.drive_letter = cleaned_letter
        else:
            raise InvalidDiskDriveError(new_letter)

    def get_drive(self):
        return self.drive_letter + ':'

    def __eq__(self, other):
        if hasattr(other, '__str__'):
            return str(self) == str(other)
        else:
            return False
    
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        return self.get_drive()

    def __repr__(self):
        return '<{cls}: {str}>'.format(cls=self.__class__.__name__, str=self.get_drive())


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
