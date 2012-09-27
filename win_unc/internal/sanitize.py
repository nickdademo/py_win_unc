"""
Functions for sanitizing Windows-specific fields.
"""


def sanitize_for_shell(string):
    """
    Return `string` with double quotes escaped for use in a shell command.
    """
    return string.replace('"', r'\"')


def sanitize_logon(name):
    """
    Removes characters from `path` that cannot be part of a valid Windows logon name or
    domain\logon name.
    """
    return name.translate(None, r'"/[]:;|=,+*?<>' + '\0')


def sanitize_path(path):
    """
    Removes characters from `path` that cannot be part of a valid Windows path.
    """
    return path.translate(None, r'<>"/|?*' + ''.join(map(chr, range(0, 31))))


def sanitize_file_name(file_name):
    """
    Removes characters from `file_name` that cannot be part of a valid Windows file name.
    """
    return sanitize_path(file_name).translate(None, ':\\')
