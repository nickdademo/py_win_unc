class UncDirectory(object):
    def __init__(self, path, username=None, password=None):
        if hasattr(path, 'path') and hasattr(path, 'username') and hasattr(path, 'password'):
            self.path = path.path
            self.username = path.username
            self.password = path.password
        else:
            self.path = path
            self.username = username
            self.password = password

    def __eq__(self, other):
        try:
            return (self.get_normalized_path() == other.get_normalized_path()
                    and self.username == other.username
                    and self.password == other.password)
        except AttributeError:
            return False

    def get_normalized_path(self):
        """
        Returns the normalized path for this `UncDirectory`. Differing UNC paths that all point to
        the same network location will have the same normalized path.
        """
        path = self.path.lower()
        return path[:-5] if path.endswith(r'\ipc$') else path.rstrip('\\')

    def __str__(self):
        return '{username}{password}{at}{path}'.format(
            username=self.username,
            password=':' + self.password if self.password else '',
            at='@' if self.username or self.password else '',
            path=self.path)

    def __repr__(self):
        return '<{cls}: {str}>'.format(cls=self.__class__.__name__, str=str(self))
