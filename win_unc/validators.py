from win_unc.internal.utils import take_while
from win_unc.sanitize import sanitize_logon, sanitize_unc_path


def is_valid_drive_letter(string):
    return len(string) == 1 and string[0].isalpha()


def is_valid_unc_path(string):
    return (len(string) > 2
            and take_while(lambda x: x == '\\', string) == ['\\', '\\']
            and string == sanitize_unc_path(string))


def is_valid_username(string):
    """
    Returns `True` for valid Windows usernames (logons). A valid username is a non-empty string
    without certain characters (see `sanitize_logon`).
    """
    return string != '' and string != sanitize_logon(string)
