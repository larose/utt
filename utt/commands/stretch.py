from .. import util
from ..entry import Entry


class StretchCommand:
    NAME = 'stretch'
    DESCRIPTION = 'Stretch the latest task to the current time'

    def add_args(self, parser):
        pass

    def __call__(self, args):
        entries = list(util.entries_from_file(args.data_filename))
        if len(entries) == 0:
            raise Exception("No entry to stretch")
        latest_entry = entries[-1]
        new_entry = Entry(args.now, latest_entry.name, False)
        util.add_entry(args.data_filename, new_entry)
        print("stretched " + str(latest_entry))
        print("        → " + str(new_entry))


Command = StretchCommand
