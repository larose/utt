import argparse
import copy
from datetime import datetime

from utt.api import _v1


class StretchHandler:
    def __init__(self, args: argparse.Namespace, now: datetime,
                 add_entry: _v1.components.AddEntry,
                 entries: _v1.components.Entries,
                 timezone_config: _v1.components.TimezoneConfig):
        self._args = args
        self._now = now
        self._add_entry = add_entry
        self._entries = entries
        self._timezone_config = timezone_config

    def __call__(self):
        entries = self._entries()
        if not entries:
            raise Exception("No entry to stretch")
        latest_entry = entries[-1]
        new_entry = _v1.types.Entry(self._now,
                                    latest_entry.name,
                                    False,
                                    comment=latest_entry.comment)
        self._add_entry(new_entry)
        print("stretched " +
              str(_localize(self._timezone_config, latest_entry)))
        print("        → " + str(_localize(self._timezone_config, new_entry)))


def _localize(timezone_config, new_entry):
    if timezone_config.enabled():
        return new_entry

    new_entry = copy.deepcopy(new_entry)
    new_entry.datetime = new_entry.datetime.replace(tzinfo=None)
    return new_entry


class StretchCommand:
    NAME = 'stretch'
    DESCRIPTION = 'Stretch the latest task to the current time'

    Handler = StretchHandler

    @staticmethod
    def add_args(parser):
        pass


_v1.add_command(StretchCommand)
