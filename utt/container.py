import sys

from . import ioc
from .activities import Activities
from .add_entry import AddEntry
from .api import _v1
from .config import config
from .config_dirname import config_dirname
from .config_filename import config_filename
from .data_dirname import data_dirname
from .data_filename import data_filename
from .default_config import DefaultConfig
from .entries import Entries
from .entry_lines import EntryLines
from .entry_parser import EntryParser
from .local_timezone import local_timezone
from .now import now
from .parse_args import parse_args
from .report import report
from .timezone_config import timezone_config


def get_commands():
    return _v1._commands  # pylint: disable=protected-access


def create_container():
    container = ioc.Container()
    container.activities = Activities
    container.add_entry = AddEntry
    container.args = parse_args
    container.commands = get_commands()
    container.config = config
    container.config_dirname = config_dirname
    container.config_filename = config_filename
    container.data_dirname = data_dirname
    container.data_filename = data_filename
    container.default_config = DefaultConfig
    container.entries = Entries
    container.entry_parser = EntryParser
    container.entry_lines = EntryLines
    container.local_timezone = local_timezone
    container.now = now
    container.output = sys.stdout
    container.report = report
    container.timezone_config = timezone_config

    for command in container.commands:
        setattr(container, 'command/{}'.format(command.NAME), command.Handler)

    return container
