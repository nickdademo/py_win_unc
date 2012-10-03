from stringlike import StringLike

from win_unc.errors import UncDirectoryError, InvalidUncPathError
from win_unc.cleaners import clean_unc_path
from win_unc.internal.utils import has_attrs
from win_unc.unc_credentials import UncCredentials, get_creds_from_string
from win_unc.validators import is_valid_unc_path


class UncDirectory(StringLike):
    def __init__(self, path, username=None, password=None):
        if username is None and password is None and has_attrs(path, 'path', 'creds'):
            self.path = path.path
            self.creds = path.creds
        else:
            self.path = clean_unc_path(path)
            self.creds = UncCredentials(username, password)

        if not is_valid_unc_path(self.path):
            raise InvalidUncPathError(self.path)

    def get_username(self):
        return self.creds.username

    def get_password(self):
        return self.creds.password

    def get_path(self):
        return self.path

    def get_normalized_path(self):
        """
        Returns the normalized path for this `UncDirectory`. Differing UNC paths that all point to
        the same network location will have the same normalized path.
        """
        path = self.path.lower()
        return path[:-5] if path.endswith(r'\ipc$') else path.rstrip('\\')

    def __eq__(self, other):
        if has_attrs(other, 'get_normalized_path', 'creds'):
            return (self.get_normalized_path() == other.get_normalized_path()
                    and self.creds == other.creds)
        elif hasattr(other, '__str__'):
            try:
                return self == get_unc_directory_from_string(str(other))
            except UncDirectoryError:
                return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        creds = self.creds.get_auth_string()
        return '{creds}{at}{path}'.format(
            creds=creds,
            at='@' if creds else '',
            path=self.path)

    def __repr__(self):
        return '<{cls}: {str}>'.format(cls=self.__class__.__name__, str=str(self))


def get_unc_directory_from_string(string):
    creds = UncCredentials()
    path = string

    if r'@\\' in string:
        creds_part, path_part = string.rsplit(r'@\\', 1)  # Always split on the last `@\\` in case
                                                          # the password contains it.
        path = r'\\' + path_part
        creds = get_creds_from_string(creds_part)

    return UncDirectory(path, creds.username, creds.password)
