from win_unc.internal.drive_letters import get_available_drive_letter


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
