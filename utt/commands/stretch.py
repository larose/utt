from .. import util
from ..entry import Entry


class StretchHandler:
    def __init__(self, args, data_filename, now):
        self._args = args
        self._data_filename = data_filename
        self._now = now

    def __call__(self):
        entries = list(util.entries_from_file(self._data_filename))
        if len(entries) == 0:
            raise Exception("No entry to stretch")
        latest_entry = entries[-1]
        new_entry = Entry(self._now, latest_entry.name, False)
        util.add_entry(self._data_filename, new_entry)
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
