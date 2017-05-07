import os
import subprocess

NAME = 'edit'
DESCRIPTION = 'Edit task log using your system\'s default editor'

def add_args(parser):
    pass

def execute(args):
    _run_editor(_editor(), args.data_filename)

def _editor():
    # CHECK $EDITOR FIRST, SINCE IT IS SET TO 'cat' FOR 'make test'.
    # AN INTERACTIVE EDITOR WILL INTERRUPT THE TEST IF $VISUAL IS SET
    # AND CHECKED FIRST.
    return (os.environ.get("EDITOR") or
            os.environ.get("VISUAL", "vi"))

def _run_editor(editor, data_filename):
    return subprocess.call("%s \"%s\"" % (editor, data_filename), shell=True)
