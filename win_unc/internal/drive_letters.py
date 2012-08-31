import os
import string

from win_unc.errors import NoDrivesAvailableError


def get_available_drive_letter():
    """
    Returns the first available Windows drive letter. The search starts with "Z" since the later
    letters are not as commonly mapped. If the system does not have any drive letters available
    this will raise a `NoDrivesAvailableError`.
    """
    for letter in reversed(string.ascii_uppercase):
        if not os.path.isdir(letter + ':\\'):
            return letter
    else:
        raise NoDrivesAvailableError()
