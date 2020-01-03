import argparse

from ..api import _v1
from ..components.add_entry import AddEntry  # Private API


class HelloHandler:
    def __init__(
        self, args: argparse.Namespace, now: _v1.Now, add_entry: AddEntry,
    ):
        self._args = args
        self._now = now
        self._add_entry = add_entry

    def __call__(self):
        self._add_entry(_v1.Entry(self._now, _v1.HELLO_ENTRY_NAME, False))


class HelloCommand:
    NAME = _v1.HELLO_ENTRY_NAME
    DESCRIPTION = "Say '{hello_entry_name}' when you arrive in the morning...".format(
        hello_entry_name=_v1.HELLO_ENTRY_NAME
    )

    Handler = HelloHandler

    @staticmethod
    def add_args(parser):
        pass


_v1.add_command(HelloCommand)
