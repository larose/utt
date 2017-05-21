import datetime
import sys
import logging
import os
import argparse
import argcomplete

from . import cmd_add, cmd_edit, cmd_hello, cmd_stretch, cmd_report
from .__version__ import version
from . import util


def main():

    logging.basicConfig(
        filename=util.utt_debug_log(),
        level=logging.DEBUG,
        format='%(asctime)s %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p')

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=
        'Ultimate Time Tracker (utt) is a simple command-line time tracking application written in Python.'
    )

    handlers = _parse_args(
        parser, [cmd_add, cmd_edit, cmd_hello, cmd_stretch, cmd_report])
    parser.add_argument(
        '--version',
        action='version',
        version="\n".join(
            ["utt {version}".format(version=version),
             "Python " + sys.version]))

    if len(sys.argv) == 1:
        sys.argv.append('--help')

    argcomplete.autocomplete(parser, append_space=False)

    args = parser.parse_args()

    handler = handlers.get(args.command)

    if handler:
        handler(args)


def _parse_args(parser, modules):
    parser.add_argument(
        "--data", dest="data_filename", default=util.utt_filename())
    parser.add_argument(
        "--now",
        dest="now",
        default=datetime.datetime.today(),
        type=util.parse_datetime)
    subparsers = parser.add_subparsers(dest="command")
    handlers = {}

    for module in modules:
        sub_parse = subparsers.add_parser(
            module.NAME, description=module.DESCRIPTION)
        module.add_args(sub_parse)
        handlers[module.NAME] = module.execute

    return handlers


if __name__ == '__main__':
    main()
