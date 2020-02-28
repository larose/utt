import argparse
import os
import subprocess

from utt.components.data_filename import DataFilename  # Private API

from ..api import _v1


class EditHandler:
    def __init__(self, args: argparse.Namespace, data_filename: DataFilename):
        self._args = args
        self._data_filename = data_filename

    def __call__(self):
        _run_editor(_editor(), self._data_filename)


edit_command = _v1.Command("edit", "Edit task log using your system's default editor", EditHandler, lambda p: None)


_v1.add_command(edit_command)


def _editor():
    return os.environ.get("VISUAL") or os.environ.get("EDITOR", "vi")


def _run_editor(editor, data_filename):
    return subprocess.call('%s "%s"' % (editor, data_filename), shell=True)
