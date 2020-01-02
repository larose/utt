import sys

from utt import ioc
from utt.components.activities import Activities
from utt.components.add_entry import AddEntry
from utt.components.config import config
from utt.components.config_dirname import config_dirname
from utt.components.config_filename import config_filename
from utt.components.data_dirname import data_dirname
from utt.components.data_filename import data_filename
from utt.components.default_config import DefaultConfig
from utt.components.entries import Entries
from utt.components.entry_lines import EntryLines
from utt.components.entry_parser import EntryParser
from utt.components.local_timezone import local_timezone
from utt.components.now import now
from utt.components.parse_args import parse_args
from utt.components.timezone_config import TimezoneConfig, timezone_config
from utt.constants import HELLO_ENTRY_NAME
from utt.data_structures.activity import Activity
from utt.data_structures.entry import Entry
from utt.data_structures.name import Name
from utt.report import report


class Types:
    Activity = Activity
    Entry = Entry
    Name = Name


class Components:
    AddEntry = AddEntry
    DefaultConfig = DefaultConfig
    Entries = Entries
    TimezoneConfig = TimezoneConfig


class V1:
    HELLO_ENTRY_NAME = HELLO_ENTRY_NAME
    types = Types
    components = Components

    def __init__(self):
        self._container = _create_container()
        self._commands = {}

    def add_command(self, command_class):
        self._commands[command_class.NAME] = command_class
        self._container.commands.append(command_class)
        setattr(
            self._container, "commands/{}".format(command_class.NAME), command_class.Handler,
        )

    @property
    def commands(self):
        return self._commands


def _create_container():
    container = ioc.Container()

    container.activities = Activities
    container.add_entry = AddEntry
    container.args = parse_args
    container.commands = []
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

    return container
