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


class EditCommand:
    NAME = "edit"
    DESCRIPTION = "Edit task log using your system's default editor"

    Handler = EditHandler

    @staticmethod
    def add_args(parser):
        pass


_v1.add_command(EditCommand)


def _editor():
    return os.environ.get("VISUAL") or os.environ.get("EDITOR", "vi")


def _run_editor(editor, data_filename):
    return subprocess.call('%s "%s"' % (editor, data_filename), shell=True)
