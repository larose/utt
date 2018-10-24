# -*- coding: utf-8 -*-
from ..entry import Entry


class StretchHandler:
    def __init__(self, args, now, log_repo):
        self._args = args
        self._now = now
        self._log_repo = log_repo

    def __call__(self):
        entries = list(self._log_repo.entries())
        if len(entries) == 0:
            raise Exception("No entry to stretch")
        latest_entry = entries[-1]
        new_entry = Entry(self._now, latest_entry.name, False)
        self._log_repo.append_entry(new_entry)
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
