import os
import subprocess

NAME = 'edit'

def add_args(parser):
    pass

def execute(args):
    _run_editor(_editor(), args.data_filename)

def _editor():
    return (os.environ.get("VISUAL") or
            os.environ.get("EDITOR", "vi"))

def _run_editor(editor, data_filename):
    return subprocess.call("%s \"%s\"" % (editor, data_filename), shell=True)
