import os
import subprocess

NAME = 'edit'
DESCRIPTION = 'Edit task log using your system\'s default editor'


def add_args(parser):
    pass


def execute(args):

    _run_editor(path_default_editor(), args.data_filename)


def checkEnvVar(envVar):

    szPath = os.environ.get(envVar, '')

    if(len(szPath) > 0):
        return szPath

    return False


def path_default_editor():

    szEditorDefault = '/usr/bin/editor'

    if(not os.path.exists(szEditorDefault)):
        szEditorDefault = 'vi'

    # NOTE: CHECK $EDITOR FIRST SINCE IT IS SET TO 'cat' ON 'make test'
    return (
        checkEnvVar("EDITOR") or
        checkEnvVar("VISUAL") or
        szEditorDefault
    )


def _run_editor(editor, data_filename):
    return subprocess.call("%s \"%s\"" % (editor, data_filename), shell=True)
