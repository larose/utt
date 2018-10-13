from .. import util
from ..entry import Entry


class HelloCommand:
    NAME = 'hello'
    DESCRIPTION = 'Say \'hello\' when you arrive in the morning...'

    def add_args(self, parser):
        pass

    def __call__(self, args):
        util.add_entry(args.data_filename, Entry(args.now, 'hello', False))


Command = HelloCommand
