"""
Functions for sanitizing various strings to be used in a shell command.
"""

from win_unc.internal.utils import take_while
from win_unc.sanitizors import sanitize_username, sanitize_unc_path


def is_valid_drive_letter(string):
    """
    Returns `True` if `string` represents a valid drive letter. Drive letters are exactly one
    character in length and between "A" and "Z". Case does not matter.
    """
    return (len(string) == 1          # Must be exactly one character long
            and string[0].isalpha())  # Must be an alphabet character (A through Z)


def is_valid_unc_path(string):
    """
    Returns `True` if `string` is a valid UNC path. Valid UNC paths are at least three characters
    long, begin with "\\", do not start or end with whitepsace, and do not contain certain invalid
    characters (see `sanitize_unc_path`).
    """
    return (len(string) > 2                           # Must be at least 3 characters
            and take_while(lambda x: x == '\\', string) == ['\\', '\\']  # Must begin with `\\`
            and string == string.strip()              # Must not have surrounding white-space
            and string == sanitize_unc_path(string))  # Must not contain invalid characters


def is_valid_username(string):
    """
    Returns `True` for valid Windows usernames (logons). A valid username is a non-empty string,
    that does not start or end with whitespace, and does not contain certain invalid characters
    (see `sanitize_username`).
    """
    return (len(string) > 0                           # Must not be empty
            and string == string.strip()              # Must not have surrounding white-space
            and string == sanitize_username(string))  # Must not contain invalid characters
