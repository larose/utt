import argparse
import sys
from configparser import ConfigParser

from ... import ioc
from ...components.activities import Activities, activities
from ...components.add_entry import AddEntry
from ...components.commands import Commands
from ...components.config import config
from ...components.config_dirname import ConfigDirname, config_dirname
from ...components.config_filename import ConfigFilename, config_filename
from ...components.data_dirname import DataDirname, data_dirname
from ...components.data_filename import DataFilename, data_filename
from ...components.default_config import DefaultConfig
from ...components.entries import Entries, entries
from ...components.entry_lines import EntryLines
from ...components.entry_parser import EntryParser
from ...components.local_timezone import LocalTimezone, local_timezone
from ...components.now import Now, now
from ...components.output import Output
from ...components.parse_args import parse_args
from ...components.timezone_config import TimezoneConfig, timezone_config
from ...report import Report, report


def create_container():
    _container = ioc.Container()

    _container[Activities] = activities
    _container[AddEntry] = AddEntry
    _container[argparse.Namespace] = parse_args
    _container[Commands] = []
    _container[ConfigParser] = config
    _container[ConfigDirname] = config_dirname
    _container[ConfigFilename] = config_filename
    _container[DataDirname] = data_dirname
    _container[DataFilename] = data_filename
    _container[DefaultConfig] = DefaultConfig
    _container[Entries] = entries
    _container[EntryParser] = EntryParser
    _container[EntryLines] = EntryLines
    _container[LocalTimezone] = local_timezone
    _container[Now] = now
    _container[Output] = sys.stdout
    _container[Report] = report
    _container[TimezoneConfig] = timezone_config

    return _container


def add_command(command_class):
    commands[command_class.NAME] = command_class
    container[Commands].append(command_class)
    container[command_class] = command_class.Handler


commands = {}
container = create_container()
