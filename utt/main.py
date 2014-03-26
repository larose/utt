import argparse
import datetime
import sys
import os

from . import cmd_add, cmd_edit, cmd_hello, cmd_report

def main():
    parser = argparse.ArgumentParser()
    handlers = _parse_args(parser, [cmd_add, cmd_edit, cmd_hello, cmd_report])

    if len(sys.argv) == 1:
        sys.argv.append('--help')

    args = parser.parse_args()
    handler = handlers.get(args.command)

    args.now = datetime.datetime.now()

    if handler:
        handler(args)

def _parse_args(parser, modules):
    parser.add_argument("--data", dest="data_filename",
                        default=_utt_filename())
    subparsers = parser.add_subparsers(dest="command")
    handlers = {}

    for module in modules:
        module.add_args(subparsers.add_parser(module.NAME))
        handlers[module.NAME] = module.execute

    return handlers

def _user_data_dir():
    return os.getenv('XDG_DATA_HOME', os.path.expanduser("~/.local/share"))

def _utt_filename():
    return os.path.join(_user_data_dir(), 'utt', 'utt.log')
