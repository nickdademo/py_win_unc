class Qualifiable(object):
    _QUALIFYING_ATTRS = []

    @classmethod
    def _qualifies(cls, other):
        return object_qualifies(other, cls._QUALIFYING_ATTRS)


def object_qualifies(obj, qualifiers):
    qualifies = True
    for qualifier in qualifiers:
        if not hasattr(obj, qualifier):
            qualifies = False
            break
    return qualifies
