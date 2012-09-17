from win_unc.internal.drive_letters import get_available_drive_letter
from win_unc.mounting import mount_unc, unmount_unc


class MountedUncDirectory(object):
    """
    A class encapsulating a UNC path to a directory and the task of mounting it.
    """

    def __init__(self, unc_path, drive_letter, username=None, password=None, persistent=False):
        """
        Returns a `UncDirectory` class. `unc_path` is a UNC path to a directory (not a file).
        `username` is the optional username to use when mounting the UNC path. `password` is the
        optional password associated with `username` to use when mounting the UNC path.

        If `persistent` is `False` the object will transparently unmount the UNC path the object
        is destroyed or when a `with` statement is exited. Otherwise, the UNC mount must be
        manually unmounted with `unmount`.
        """
        self._unc_path = unc_path
        self._username = username
        self._password = password
        self._drive_letter = None
        self._persistent = persistent

    def get_path(self):
        """
        Ensures the UNC directory is mounted and returns a local path to the directory where it is
        mounted.
        """
        self.mount()
        return self._drive_letter + ':\\'

    def is_mounted(self):
        """
        Returns `True` if the UNC directory is mounted and `False` if not.
        """
        return self._drive_letter is not None

    def mount(self):
        """
        Mounts the UNC directory to an available drive letter. Nested calls to this function will
        be counted, thus requiring a symmetric number of calls to `unmount()`.
        """
        if not self.is_mounted():
            drive_letter = get_available_drive_letter()
            if mount_unc(self._path, drive_letter, self._username, self._password):
                self._drive_letter = drive_letter
            else:
                raise UncMountingError(self._path, drive_letter)

    def unmount(self):
        """
        Unmounts the UNC directory or decrements the count of the number of calls to `mount()`.
        """
        if self.is_mounted():
            if unmount_unc(self._drive_letter):
                self._drive_letter = None

    def __del__(self):
        if not self._persistent:
            self.unmount()


def is_unc_directory(path, allow_auth=True):
    """
    Returns `True` for instances of `path` that are UNC paths. It also supports "HTTP Basic
    Authentication"-styled UNC paths.
    """
    unc_part, _ = os.path.splitunc(path)
    return (allow_auth and '@\\\\' in path) or len(unc_part) > 0


def get_unc_directory(unc_path, allow_auth=True):
    """
    Returns a `UncDirectory` with the location `unc_path`.

    If `allow_auth` is `True` then `unc_path` may include an "HTTP Baisc Authentication"-styled
    prefix which includes the username and/or password to use for authenticating with the UNC
    path.

    The following are examples of valid UNC paths accepted by this function with `allow_auth` set
    to `True`:
      * \\remote.unc.path\directory  # UNC path with no authentication
      * username@\\remote.unc.path\directory  # UNC path using "username" for authentication
      * username:password@\\remote.unc.path\directory  # UNC path using "username" and "password"
                                                       # for authentication
    """
    username = None
    password = None
    path_part = unc_path

    if allow_auth and '@' in unc_path:
        auth_part, path_part = unc_path.split('@', 1)
        if ':' in auth_part:
            username, password = auth_part.split(':', 1)
        else:
            username = auth_part

    return UncDirectory(path_part, username, password)
