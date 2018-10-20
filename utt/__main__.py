import datetime
import sys
import os
import argparse
import argcomplete

from . import util
from . import ioc
from .__version__ import version
from .commands import add, edit, hello, stretch, report
from .entry_parser import EntryParser
from .data_dirname import data_dirname
from .data_filename import data_filename
from .log_repo import LogRepo
from .now import now
from .timezone_config import timezone_config

COMMAND_MODULES = [add, edit, hello, stretch, report]


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=
        'Ultimate Time Tracker (utt) is a simple command-line time tracking application written in Python.'
    )

    argcomplete.autocomplete(parser, append_space=False)

    parser.add_argument("--data", dest="data_filename")

    parser.add_argument("--now", dest="now", type=util.parse_datetime)

    parser.add_argument(
        '--version',
        action='version',
        version="\n".join(
            ["utt {version}".format(version=version),
             "Python " + sys.version]))

    subparsers = parser.add_subparsers(dest="command")

    for module in COMMAND_MODULES:
        command = module.Command
        sub_parser = subparsers.add_parser(
            command.NAME, description=command.DESCRIPTION)
        command.add_args(sub_parser)

    return parser.parse_args()


def main():
    if len(sys.argv) == 1:
        sys.argv.append('--help')

    container = ioc.Container()
    container.args = parse_args
    container.data_dirname = data_dirname
    container.data_filename = data_filename
    container.entry_parser = EntryParser
    container.now = now
    container.log_repo = LogRepo
    container.timezone_config = timezone_config

    for module in COMMAND_MODULES:
        setattr(container, module.Command.NAME, module.Command.Handler)

    getattr(container, container.args.command)()


if __name__ == '__main__':
    main()
