# -*- coding: utf-8 -*-
from ..entry import Entry


class StretchHandler:
    def __init__(self, args, now, add_entry, entries):
        self._args = args
        self._now = now
        self._add_entry = add_entry
        self._entries = entries

    def __call__(self):
        entries = self._entries()
        if not entries:
            raise Exception("No entry to stretch")
        latest_entry = entries[-1]
        new_entry = Entry(self._now, latest_entry.name, False)
        self._add_entry(new_entry)
        print("stretched " + str(latest_entry))
        print("        → " + str(new_entry))


class StretchCommand:
    NAME = 'stretch'
    DESCRIPTION = 'Stretch the latest task to the current time'

    Handler = StretchHandler

    @staticmethod
    def add_args(parser):
        pass


Command = StretchCommand
