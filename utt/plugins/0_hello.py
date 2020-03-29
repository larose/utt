import argparse

from ..api import _v1


class HelloHandler:
    def __init__(
        self, args: argparse.Namespace, now: _v1.Now, add_entry: _v1._private.AddEntry,
    ):
        self._args = args
        self._now = now
        self._add_entry = add_entry

    def __call__(self):
        self._add_entry(_v1.Entry(self._now, _v1.HELLO_ENTRY_NAME, False))


hello_command = _v1.Command(
    "hello",
    "Say '{hello_entry_name}' when you arrive in the morning...".format(hello_entry_name=_v1.HELLO_ENTRY_NAME),
    HelloHandler,
    lambda p: None,
)

_v1.register_command(hello_command)
