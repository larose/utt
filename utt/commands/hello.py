from ..entry import Entry


class HelloHandler:
    def __init__(self, args, now, add_entry):
        self._args = args
        self._now = now
        self._add_entry = add_entry

    def __call__(self):
        self._add_entry(Entry(self._now, 'hello', False))


class HelloCommand:
    NAME = 'hello'
    DESCRIPTION = 'Say \'hello\' when you arrive in the morning...'

    Handler = HelloHandler

    @staticmethod
    def add_args(parser):
        pass


Command = HelloCommand
