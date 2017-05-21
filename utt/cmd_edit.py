import os
import subprocess

NAME = 'edit'
DESCRIPTION = 'Edit task log using your system\'s default editor'


def add_args(parser):
    pass


def execute(args):
    _run_editor(_editor(), args.data_filename)


def _editor():
    # Check $EDITOR first, since it is set to 'cat' for 'make test'.
    # an interactive editor will interrupt the test if $visual is set
    # and checked first.
    return (os.environ.get("EDITOR") or os.environ.get("VISUAL", "vi"))


def _run_editor(editor, data_filename):
    return subprocess.call("%s \"%s\"" % (editor, data_filename), shell=True)
