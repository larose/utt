import itertools

from .activity import Activity
from .commands import hello


class Activities:
    def __init__(self, entries):
        self._entries = entries

    def __call__(self):
        return list(self._activities())

    def _activities(self):
        for prev_entry, next_entry in _pairwise(self._entries()):
            if next_entry.name == hello.HelloCommand.NAME:
                continue

            activity = Activity(next_entry.name, prev_entry.datetime,
                                next_entry.datetime, False)
            yield activity


# pylint: disable=invalid-name
def _pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)
