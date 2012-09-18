"""
Contains classes for dealing with UNC paths on Windows.
"""


from win_unc.internal.loggers import no_logging
from win_unc.internal.net_use_table import parse_net_use_table
from win_unc.internal.sanitize import sanitize_for_shell, sanitize_logon, sanitize_path
from win_unc.internal.shell import run, ShellCommandError


class UncDirectoryMount(object):
    def __init__(self, unc_dir, drive_letter, persistent=False, logger=no_logging):
        self.unc_dir = unc_dir
        self.drive_letter = drive_letter
        self.logger = logger

    def mount(self):
        """
        Mounts the `unc_path` at `drive_letter` using `username` and/or `password` as credentials (if
        supplied). It first tries to mount the drive without credentials. If that fails (and
        credentials were provided), it tries again with credentials. If both fail, this will raise a
        `ShellCommandError`.
        """
        self.logger('Mounting the network UNC path "{path}" to the {drive}: drive.'.format(
            path=self.unc_path,
            drive=self.drive_letter))

        try:
            # First try without any credentials.
            self._run_mounting_command()
        except ShellCommandError:
            # The first attempt failed. If credentials were provided, try them. Otherwise re-raise the
            # error.
            if username or password:
                run_mounting_command(self.username, self.password)
            else:
                raise

    def unmount(self):
        """
        Unmounts the UNC path mounted at `drive_letter`. If the command fails, this will raise a
        `ShellCommandError`.
        """
        self.logger('Unmounting the {drive}: network drive.'.format(drive=self.drive_letter))
        run('NET USE {drive}: /DELETE /YES'.format(drive=self.drive_letter))

    def is_mounted(self):
        net_use_table = self._get_current_net_use_table()
        matching_row = net_use_table.get_matching_rows('local': self.drive_letter + ':', 'remote': self.unc_path)

    def _get_mounting_command(self, username=None, password=None):
        """
        Returns the Windows command to be used to mount `unc_path` to `drive_letter`. `username` and/or
        `password` are used as credentials if they are supplied.
        """
        return 'NET USE {drive}: "{path}" "{password}" /USER:"{user}" /PERSISTENT:{persistent}'.format(
            drive=sanitize_for_shell(self.drive_letter),
            path=sanitize_path(self.unc_path),
            password=sanitize_for_shell(password) if password else '',
            user=sanitize_logon(username) if username else '',
            persistent='YES' if self.persistent else 'NO')

    def _run_mounting_command(self, username=None, password=None):
        """
        Constructs and executes the Windows mounting command to mount `unc_path` to `drive_letter`.
        `username` and/or `password` are used as credentials if they are supplied. If there is an error
        a `ShellCommandError` is raised.
        """
        masked_password = '-----' if password else None
        self.logger(self._get_mounting_command(username, masked_password))
        run(self.get_mounting_command(username, password))

    def _get_current_net_use_table(self):
        stdout, _ = run('NET USE')
        return parse_net_use_table(stdout)


class UncDirectory(object):
    def __init__(self, unc_path, username=None, password=None):
        self.unc_path = unc_path
        self.username = username
        self.password = password

    def get_mount(self, drive_letter, persistent=False):
        return UncDirectoryMount(self, drive_letter, persistent)



