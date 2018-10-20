from ..entry import Entry


class HelloHandler:
    def __init__(self, args, now, log_repo):
        self._args = args
        self._now = now
        self._log_repo = log_repo

    def __call__(self):
        self._log_repo.append_entry(Entry(self._now, 'hello', False))


class HelloCommand:
    NAME = 'hello'
    DESCRIPTION = 'Say \'hello\' when you arrive in the morning...'

    Handler = HelloHandler

    @staticmethod
    def add_args(parser):
        pass


Command = HelloCommand
