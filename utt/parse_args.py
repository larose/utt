import argparse
import datetime
import sys
import argcomplete
import pytz

from .commands import COMMAND_MODULES
from .__version__ import VERSION


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='Ultimate Time Tracker (utt) is a simple command-line time'
        ' tracking application written in Python.')

    argcomplete.autocomplete(parser, append_space=False)

    parser.add_argument("--data", dest="data_filename")

    parser.add_argument("--now", dest="now", type=parse_datetime)

    parser.add_argument("--timezone", dest="timezone", type=pytz.timezone)

    parser.add_argument(
        '--version',
        action='version',
        version="\n".join(
            ["utt {version}".format(version=VERSION),
             "Python " + sys.version]))

    subparsers = parser.add_subparsers(dest="command")

    for module in COMMAND_MODULES:
        command = module.Command
        sub_parser = subparsers.add_parser(
            command.NAME, description=command.DESCRIPTION)
        command.add_args(sub_parser)

    return parser.parse_args()


def parse_datetime(datetimestring):
    return datetime.datetime.strptime(datetimestring, "%Y-%m-%d %H:%M")
