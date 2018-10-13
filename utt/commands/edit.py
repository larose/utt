import os
import subprocess


class EditCommand:
    NAME = 'edit'
    DESCRIPTION = 'Edit task log using your system\'s default editor'

    def add_args(self, parser):
        pass

    def __call__(self, args):
        _run_editor(_editor(), args.data_filename)


Command = EditCommand


def _editor():
    return (os.environ.get("VISUAL") or os.environ.get("EDITOR", "vi"))


def _run_editor(editor, data_filename):
    return subprocess.call("%s \"%s\"" % (editor, data_filename), shell=True)
