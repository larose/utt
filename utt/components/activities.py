import itertools
from typing import List

from ..data_structures.activity import Activity
from .entries import Entries

Activities = List[Activity]


def activities(entries: Entries) -> Activities:
    return list(_activities(entries))


def _activities(entries: Entries):
    for prev_entry, next_entry in _pairwise(entries):
        activity = Activity(
            next_entry.name, prev_entry.datetime, next_entry.datetime, False, comment=next_entry.comment,
        )
        yield activity


def _pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)
