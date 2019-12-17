# -*- coding: utf-8 -*-
import copy

from ..entry import Entry


class StretchHandler:
    # pylint: disable=too-many-arguments
    def __init__(self, args, now, add_entry, entries, timezone_config):
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
        new_entry = Entry(self._now,
                          latest_entry.name,
                          False,
                          comment=latest_entry.comment)
        self._add_entry(new_entry)
        print("stretched " +
              str(_localize(self._timezone_config, latest_entry)))
        print("        → " + str(_localize(self._timezone_config, new_entry)))


class StretchCommand:
    NAME = 'stretch'
    DESCRIPTION = 'Stretch the latest task to the current time'

    Handler = StretchHandler

    @staticmethod
    def add_args(parser):
        pass


Command = StretchCommand


def _localize(timezone_config, new_entry):
    if timezone_config.enabled():
        return new_entry

    new_entry = copy.deepcopy(new_entry)
    new_entry.datetime = new_entry.datetime.replace(tzinfo=None)
    return new_entry
