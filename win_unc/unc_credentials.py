from win_unc.errors import InvalidUsernameError
from win_unc.cleaners import clean_username
from win_unc.internal.utils import has_attrs
from win_unc.validators import is_valid_username


class UncCredentials(object):
    def __init__(self, username=None, password=None):
        if password is None and has_attrs(username, 'username', 'password'):
            new_username = username.username
            new_password = username.password
        else:
            new_username = username
            new_password = password

        cleaned_username = clean_username(new_username) if new_username is not None else None

        if cleaned_username is None or is_valid_username(cleaned_username):
            self.username = cleaned_username
            self.password = new_password
        else:
            raise InvalidUsernameError(new_username)

    def get_auth_string(self):
        if self.password is not None:
            return '{0}:{1}'.format(self.username or '', self.password)
        elif self.username:
            return self.username
        else:
            return ''

    def __eq__(self, other):
        if has_attrs(other, 'username', 'password'):
            return self.username == other.username and self.password == other.password
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return '<{cls}: "{str}">'.format(cls=self.__class__.__name__, str=self.get_auth_string())


def get_creds_from_string(string):
    username, password = None, None

    if ':' in string:
        username, password = string.split(':', 1)  # Always split on the first `:` in case the
                                                   # password contains it.
    else:
        username = string

    return UncCredentials(username or None, password)  # Usernames cannot be `''`, but password can be.
