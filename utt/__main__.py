import datetime
import sys
import os
import argparse
import argcomplete
import re

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
from .local_timezone import local_timezone

COMMAND_MODULES = [add, edit, hello, stretch, report]

TIMEZONE_OFFSET_REGEX = re.compile("(?P<sign>[+-]{0,1})(?P<hours>\d{2}):{0,1}(?P<minutes>\d{2})")

def parse_timezone_offset(string):
    match = TIMEZONE_OFFSET_REGEX.match(string)
    if match is None:
        raise Exception("Invalid timezone offset {}".format(string))

    groupdict = match.groupdict()

    delta = datetime.timedelta(
        hours=int(groupdict['hours']),
        minutes=int(groupdict['minutes'])
    )

    if groupdict['sign'] == '-':
        delta = -delta

    timezone = datetime.timezone(delta)

    return timezone


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=
        'Ultimate Time Tracker (utt) is a simple command-line time tracking application written in Python.'
    )

    argcomplete.autocomplete(parser, append_space=False)

    parser.add_argument("--data", dest="data_filename")

    parser.add_argument("--now", dest="now", type=util.parse_datetime)

    parser.add_argument("--timezone-offset", dest="timezone_offset", type=parse_timezone_offset)

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
    container.local_timezone = local_timezone
    container.log_repo = LogRepo
    container.timezone_config = timezone_config

    for module in COMMAND_MODULES:
        setattr(container, module.Command.NAME, module.Command.Handler)

    getattr(container, container.args.command)()


if __name__ == '__main__':
    main()
