"""
Functions for "cleaning" various pieces needed to make UNC connections. "Cleaning" refers to
removing or changing characters in a string without changing its meaning.
"""


def clean_drive_letter(string):
    return string.strip().rstrip(':\\').upper()


def clean_username(string):
    return string.strip()


def clean_unc_path(string):
    return string.strip().rstrip('\\')
