from ..entry import Entry


class AddHandler:
    def __init__(self, args, data_filename, now, add_entry):
        self._args = args
        self._data_filename = data_filename
        self._now = now
        self._add_entry = add_entry

    def __call__(self):
        self._add_entry(
            Entry(self._now,
                  self._args.name,
                  False,
                  comment=self._args.comment))


class AddCommand:
    NAME = 'add'
    DESCRIPTION = 'Add a completed task'

    Handler = AddHandler

    @staticmethod
    def add_args(parser):
        parser.add_argument("name", help="completed task description")
        parser.add_argument("-c",
                            "--comment",
                            help="comment/annotation for task entry")


Command = AddCommand
