from ..entry import Entry


class AddHandler:
    def __init__(self, args, data_filename, now, log_repo):
        self._args = args
        self._data_filename = data_filename
        self._now = now
        self._log_repo = log_repo

    def __call__(self):
        self._log_repo.append_entry(Entry(self._now, self._args.name, False))


class AddCommand:
    NAME = 'add'
    DESCRIPTION = 'Add a completed task'

    Handler = AddHandler

    @staticmethod
    def add_args(parser):
        parser.add_argument("name", help="completed task description")


Command = AddCommand
