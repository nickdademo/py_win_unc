from win_unc.errors import UncDirectoryError, InvalidUncPathError
from win_unc.cleaners import clean_unc_path
from win_unc.unc_credentials import UncCredentials, get_creds_from_string
from win_unc.validators import is_valid_unc_path


class UncDirectory(object):
    def __init__(self, path, creds=None):
        if creds is None and isinstance(path, UncDirectory):
            new_path = path.path
            new_creds = path.creds
        else:
            new_path = path
            new_creds = creds

        cleaned_path = clean_unc_path(new_path)
        if is_valid_unc_path(cleaned_path):
            self.path = cleaned_path
            self.creds = new_creds
        else:
            raise InvalidUncPathError(new_path)

        if self.get_username() is None and self.get_password() is None:
            self.creds = None

    def get_normalized_path(self):
        """
        Returns the normalized path for this `UncDirectory`. Differing UNC paths that all point to
        the same network location will have the same normalized path.
        """
        path = self.path.lower()
        return path[:-5] if path.endswith(r'\ipc$') else path.rstrip('\\')

    def get_username(self):
        return self.creds.username if self.creds else None

    def get_password(self):
        return self.creds.password if self.creds else None

    def get_auth_string(self):
        return self.creds.get_auth_string() if self.creds else ''

    def get_auth_path(self):
        creds = self.get_auth_string()
        return '{creds}{at}{path}'.format(
            creds=creds,
            at='@' if creds else '',
            path=self.path)

    def __eq__(self, other):
        if isinstance(other, UncDirectory):
            return (self.get_normalized_path() == other.get_normalized_path()
                    and self.creds == other.creds)
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        return self.get_auth_path()

    def __repr__(self):
        return '<{cls}: "{str}">'.format(cls=self.__class__.__name__, str=self.get_auth_path())


def get_unc_directory_from_string(string):
    creds = None
    path = string

    if r'@\\' in string:
        creds_part, path_part = string.rsplit(r'@\\', 1)  # Always split on the last `@\\` in case
                                                          # the password contains it.
        path = r'\\' + path_part
        creds = get_creds_from_string(creds_part)

    return UncDirectory(path, creds)
