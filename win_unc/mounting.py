"""
Contains classes for dealing with UNC paths on Windows.
"""


from win_unc.internal.shell import run, ShellCommandError
from win_unc.internal.loggers import no_logging



def get_mounting_command(unc_path, drive_letter, username=None, password=None):
    """
    Returns the Windows command to be used to mount `unc_path` to `drive_letter`. `username` and/or
    `password` are used as credentials if they are supplied.
    """
    return 'NET USE {drive}: {path}{password}{user} /PERSISTENT:NO'.format(
        drive=drive_letter,
        path=unc_path,
        password=' ' + password if password else '',
        user=' /USER:' + username if username else '')


def run_mounting_command(unc_path, drive_letter, username=None, password=None, logger=no_logging):
    """
    Constructs and executes the Windows mounting command to mount `unc_path` to `drive_letter`.
    `username` and/or `password` are used as credentials if they are supplied. If there is an error
    a `ShellCommandError` is raised.
    """
    masked_password = '*****' if password else None
    logger(get_mounting_command(unc_path, drive_letter, username, masked_password))
    run(get_mounting_command(unc_path, drive_letter, username, password))


def mount_unc(unc_path, drive_letter, username=None, password=None, logger=no_logging):
    """
    Mounts the `unc_path` at `drive_letter` using `username` and/or `password` as credentials (if
    supplied). It first tries to mount the drive without credentials. If that fails (and
    credentials were provided), it tries again with credentials. If both fail, this will raise a
    `ShellCommandError`.
    """
    logger('Mounting the network UNC path "{path}" to the {drive}: drive.'.format(
        path=unc_path,
        drive=drive_letter))

    try:
        # First try without any credentials
        run_mounting_command(unc_path, drive_letter)
    except ShellCommandError:
        # The first attempt failed. If credentials were provided, try them. Otherwise re-raise the
        # error.
        if username or password:
            run_mounting_command(unc_path, drive_letter, username, password)
        else:
            raise


def unmount_unc(drive_letter, logger=no_logging):
    """
    Unmounts the UNC path mounted at `drive_letter`. If the command fails, this will raise a
    `ShellCommandError`.
    """
    logger('Unmounting the {drive}: network drive.'.format(drive=drive_letter))
    run('NET USE {drive}: /DELETE /YES'.format(drive=drive_letter))
