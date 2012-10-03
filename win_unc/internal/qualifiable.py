class Qualifiable(object):
    _QUALIFYING_ATTRS = []

    def _qualifies(self, other):
        return object_qualifies(other, self._QUALIFYING_ATTRS)


def object_qualifies(obj, qualifiers):
    qualifies = True
    for qualifier in qualifiers:
        if not hasattr(obj, qualifier):
            qualifies = False
            break
    return qualifies
