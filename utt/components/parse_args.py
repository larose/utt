import argparse
import datetime
import sys

import argcomplete
import pytz

from ..__version__ import VERSION
from .commands import Commands


def parse_args(commands: Commands) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description="Ultimate Time Tracker (utt) is a simple command-line time"
        " tracking application written in Python.",
    )

    parser.add_argument("--data", dest="data_filename")

    parser.add_argument("--now", dest="now", type=parse_datetime)

    parser.add_argument("--timezone", dest="timezone", type=pytz.timezone)

    parser.add_argument(
        "--version",
        action="version",
        version="\n".join(["utt {version}".format(version=VERSION), "Python " + sys.version]),
    )

    subparsers = parser.add_subparsers(dest="command")

    for command in commands:
        sub_parser = subparsers.add_parser(command.name, description=command.description)
        command.add_args(sub_parser)

    argcomplete.autocomplete(parser, append_space=False)
    return parser.parse_args()


def parse_datetime(datetimestring):
    return datetime.datetime.strptime(datetimestring, "%Y-%m-%d %H:%M")
