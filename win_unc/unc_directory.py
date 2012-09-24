class UncDirectory(object):
    def __init__(self, path, username=None, password=None):
        self.path = path
        self.username = username
        self.password = password

    def __eq__(self, other):
        try:
            return (self.path.lower() == other.path.lower()
                    and self.username == other.username
                    and self.password == other.password)
        except AttributeError:
            return False

    def __str__(self):
        return '{username}{password}{at}{path}'.format(
            username=self.username,
            password=':' + self.password if self.password else '',
            at='@' if self.username or self.password else '',
            path=self.path)

    def __repr__(self):
        return '<{cls}: {str}>'.format(cls=self.__class__.__name__, str=str(self))