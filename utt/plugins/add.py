import argparse

from ..api import _v1
from ..components.add_entry import AddEntry  # Private API
from ..components.data_filename import DataFilename  # Private API


class AddHandler:
    def __init__(
        self, args: argparse.Namespace, data_filename: DataFilename, now: _v1.Now, add_entry: AddEntry,
    ):
        self._args = args
        self._data_filename = data_filename
        self._now = now
        self._add_entry = add_entry

    def __call__(self):
        self._add_entry(_v1.Entry(self._now, self._args.name, False, comment=self._args.comment))


class AddCommand:
    NAME = "add"
    DESCRIPTION = "Add a completed task"

    Handler = AddHandler

    @staticmethod
    def add_args(parser):
        parser.add_argument("name", help="completed task description")
        parser.add_argument("-c", "--comment", help="comment/annotation for task entry")


_v1.add_command(AddCommand)
