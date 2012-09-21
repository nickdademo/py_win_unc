"""
Contains classes for dealing with UNC paths on Windows.
"""

from win_unc.internal.loggers import no_logging
from win_unc.internal.net_use_table import parse_net_use_table
from win_unc.internal.sanitize import sanitize_for_shell, sanitize_logon, sanitize_path
from win_unc.internal.shell import run, ShellCommandError


class UncDirectory(object):
    def __init__(self, path, username=None, password=None):
        self.path = path
        self.username = username
        self.password = password

    def get_mount(self, drive_letter, persistent=False):
        return UncDirectoryMount(self, drive_letter, persistent)


class UncDirectoryConnection(object):
    def __init__(self, unc, drive_letter=None, persistent=False, logger=no_logging):
        self.unc = unc
        self.drive_letter = drive_letter
        self.persistent = persistent
        self.logger = logger

    def connect(self):
        """
        Connects the UNC directory. This will make at most three connection attempts with different
        credential configurations in case the credentials provided are not necessary (which is
        likely when the credentials are saved by Windows from a previous connection).
        """
        self.logger('Connecting the network UNC path "{path}".'.format(path=self.unc_path))

        cred_attempts = [(None, None)]
                      + [(self.unc.username, None)] if self.unc.username else []
                      + [(self.unc.username, self.unc.password)] if self.unc.password else []

        for idx, (username, password) in enumerate(cred_attempts):
            try:
                self.connect_with_creds(username, password)
                break
            except ShellCommandError:
                if idx == length(cred_attempts) - 1:
                    raise  # Raise the error if this was the last attempt

    def disconnect(self):
        """
        Unmounts the UNC path mounted at `drive_letter`. If the command fails, this will raise a
        `ShellCommandError`.
        """
        self.logger('Unmounting the {drive}: network drive.'.format(drive=self.drive_letter))
        run('NET USE {drive}: /DELETE /YES'.format(drive=self.drive_letter))

    def is_connected(self):
        net_use_table = self._get_current_net_use_table()
        matching_row = net_use_table.get_matching_rows('local': self.drive_letter + ':', 'remote': self.unc_path)

    def get_connection_command(self, username=None, password=None):
        """
        Returns the Windows command to be used to mount `unc_path` to `drive_letter`. `username` and/or
        `password` are used as credentials if they are supplied.
        """
        return 'NET USE "{drive}" "{path}" "{password}" /USER:"{user}" /PERSISTENT:{persistent}'.format(
            drive=sanitize_path(self.drive_letter.rstrip(':')) + ':' if self.drive_letter else '',
            path=sanitize_path(self.unc.path.rstrip('\\')),
            password=sanitize_for_shell(password) if password else '',
            user=sanitize_logon(username) if username else '',
            persistent='YES' if drive_letter and persistent else 'NO')

    def connect_with_creds(self, username=None, password=None):
        """
        Constructs and executes the Windows mounting command to mount `unc_path` to `drive_letter`.
        `username` and/or `password` are used as credentials if they are supplied. If there is an error
        a `ShellCommandError` is raised.
        """
        command = self.get_connection_command(username, password)
        logger(self.get_connection_command(username, '-----') if password else command)
        run(command)

    def _get_current_net_use_table(self):
        stdout, _ = run('NET USE')
        return parse_net_use_table(stdout)


class UncDirectoryMount(object):
    def __init__(self, unc, drive_letter, persistent=False, logger=no_logging):
        super(self, UncDirectoryMount).__init__(unc, drive_letter, persistent, logger)

    def mount(self):
        self.connect()

    def unmount(self):
        self.disconnect()

    def is_mounted(self):
        return self.is_connected()
