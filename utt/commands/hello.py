from .. import util
from ..entry import Entry


class HelloHandler:
    def __init__(self, args, data_filename, now):
        self._args = args
        self._data_filename = data_filename
        self._now = now

    def __call__(self):
        util.add_entry(self._data_filename, Entry(self._now, 'hello', False))


class HelloCommand:
    NAME = 'hello'
    DESCRIPTION = 'Say \'hello\' when you arrive in the morning...'

    Handler = HelloHandler

    @staticmethod
    def add_args(parser):
        pass


Command = HelloCommand
