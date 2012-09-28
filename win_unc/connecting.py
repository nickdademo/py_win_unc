"""
Contains classes for dealing with UNC paths on Windows.
"""

from win_unc.disk_drive import get_available_disk_drive
from win_unc.internal import sanitize as S
from win_unc.internal.loggers import no_logging
from win_unc.internal.net_use_table import parse_net_use_table
from win_unc.internal.shell import run, ShellCommandError
from win_unc.internal.utils import catch


class UncDirectoryConnection(object):
    def __init__(self, unc, disk_drive=None, persistent=False, logger=no_logging):
        """
        `unc` is a `UncDirectory` that describes the UNC path and necessary credentials (if
              needed).
        `disk_drive` is a drive letter between 'D' and 'Z'. This is where the UNC path will be
                       mounted when `mount()` is called. If `disk_drive` is `None`, then one of
                       the available drive letters on the system will be selected or
                       `NoDrivesAvailableError` will be raised.
        `persistent` must be `True` if the UNC drive should be mounted such that it is persists
                     across logins of the current Windows user.
        """
        self.unc = unc
        self.disk_drive = disk_drive
        self.persistent = persistent
        self.logger = logger

    def get_path(self):
        return self.unc.get_path()

    def get_username(self):
        return self.unc.get_username()

    def get_password(self):
        return self.unc.get_password()

    def connect(self):
        """
        Connects the UNC directory. This will make at most three connection attempts with different
        credential configurations in case the credentials provided are not necessary (which is
        likely when the credentials are saved by Windows from a previous connection).
        """
        self.logger('Connecting the network UNC path "{path}".'.format(path=self.unc.path))

        username = self.get_username()
        password = self.get_password()

        error = catch(self.connect_with_creds)
        if error and username:
            error = catch(self.connect_with_creds, username)
        if error and username and password:
            error = catch(self.connect_with_creds, username, password)
        if error:
            raise error

    def disconnect(self):
        """
        Unmounts the UNC path mounted at `disk_drive`. If the command fails, this will raise a
        `ShellCommandError`.
        """
        identifier = self.disk_drive or S.sanitize_path(self.unc.get_normalized_path())
        self.logger('Disconnecting the network UNC path "{path}".'.format(path=self.unc.path))
        run('NET USE "{id}" /DELETE /YES'.format(id=identifier), self.logger)

    def is_connected(self):
        net_use = get_current_net_use_table()
        matching_rows = net_use.get_matching_rows(local=self.disk_drive, remote=self.unc.path)
        if matching_rows:
            status = matching_rows[0]['status']
            return status.lower() in ['ok', 'disconnected']
        else:
            return False

    def get_connection_command(self, username=None, password=None):
        """
        Returns the Windows command to be used to connect this UNC directory.
        `username` and/or `password` are used as credentials if they are supplied.
        """
        device_str = ' "{0}"'.format(self.disk_drive) if self.disk_drive else ''
        password_str = ' "{0}"'.format(S.sanitize_for_shell(password)) if password else ''
        user_str = ' /USER:"{0}"'.format(S.sanitize_logon(username)) if username else ''

        return 'NET USE{device} "{path}"{password}{user} /PERSISTENT:{persistent}'.format(
            device=device_str,
            path=S.sanitize_path(self.unc.get_normalized_path()),
            password=password_str,
            user=user_str,
            persistent='YES' if self.disk_drive and persistent else 'NO')

    def connect_with_creds(self, username=None, password=None):
        """
        Constructs and executes the Windows mounting command to mount `unc_path` to `drive_letter`.
        `username` and/or `password` are used as credentials if they are supplied. If there is an error
        a `ShellCommandError` is raised.
        """
        command = self.get_connection_command(username, password)
        self.logger(self.get_connection_command(username, '-----') if password else command)
        run(command)

    def __str__(self):
        return str(self.unc)

    def __repr__(self):
        return '<{cls}: {str}>'.format(cls=self.__clas__.__name__, str=str(self))


class UncDirectoryMount(UncDirectoryConnection):
    def __init__(self, unc, disk_drive=None, persistent=False, logger=no_logging):
        """
        Creates a `UncDirectoryConnection` with a target mount point (drive letter).
        `unc` is a `UncDirectory` that describes the UNC path and necessary credentials (if
              needed).
        `disk_drive` is a drive letter between 'D' and 'Z'. This is where the UNC path will be
                       mounted when `mount()` is called. If `disk_drive` is `None`, then one of
                       the available drive letters on the system will be selected or
                       `NoDrivesAvailableError` will be raised.
        `persistent` must be `True` if the UNC drive should be mounted such that it is persists
                     across logins of the current Windows user.
        """
        disk_drive = disk_drive if disk_drive else get_available_disk_drive()
        super(self, UncDirectoryMount).__init__(unc, disk_drive, persistent, logger)

    def mount(self):
        self.connect()

    def unmount(self):
        self.disconnect()

    def is_mounted(self):
        return self.is_connected()


def get_current_net_use_table(logger=no_logging):
    stdout, _ = run('NET USE', logger)
    return parse_net_use_table(stdout)
