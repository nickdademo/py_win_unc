"""
Functions for sanitizing Windows-specific fields.
"""


def sanitize_path(path):
    """
    Removes characters from `path` that cannot be part of a valid Windows path.
    """
    return path.translate(None, r'<>"/|?*' + map(chr, range(0, 31)))


def sanitize_logon(name):
    """
    Removes characters from `path` that cannot be part of a valid Windows logon name or
    domain\logon name.
    """
    return name.translate(None, r'"/[]:;|=,+*?<>' + '\0')


def sanitize_for_shell(password):
    """
    Return `password` with double quotes escaped for use in a shell command.
    """
    return password.replace('"', r'\"')
