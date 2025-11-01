import argparse

from ..api import _v1
from ..components.add_entry import AddEntry  # Private API


class StretchHandler:
    def __init__(
        self,
        args: argparse.Namespace,
        now: _v1.Now,
        add_entry: AddEntry,
        entries: _v1.Entries,
        output: _v1.Output,
    ):
        self._args = args
        self._now = now
        self._add_entry = add_entry
        self._entries = entries
        self._output = output

    def __call__(self):
        if not self._entries:
            raise Exception("No entry to stretch")
        latest_entry = self._entries[-1]
        new_entry = _v1.Entry(self._now, latest_entry.name, False, comment=latest_entry.comment)
        self._add_entry(new_entry)
        print("stretched " + str(latest_entry), file=self._output)
        print("        → " + str(new_entry), file=self._output)


stretch_command = _v1.Command(
    name="stretch",
    description="Stretch the latest task to the current time",
    handler_class=StretchHandler,
    add_args=lambda p: None,
)


_v1.register_command(stretch_command)
