import sys

from . import ioc
from .commands import COMMAND_MODULES
from .entry_parser import EntryParser
from .data_dirname import data_dirname
from .data_filename import data_filename
from .add_entry import AddEntry
from .now import now
from .timezone_config import timezone_config
from .local_timezone import local_timezone
from .config_dirname import config_dirname
from .config_filename import config_filename
from .config import config
from .default_config import DefaultConfig
from .parse_args import parse_args
from .entries import Entries
from .activities import Activities
from .report import report

CONTAINER = ioc.Container()
CONTAINER.activities = Activities
CONTAINER.add_entry = AddEntry
CONTAINER.args = parse_args
CONTAINER.config = config
CONTAINER.config_dirname = config_dirname
CONTAINER.config_filename = config_filename
CONTAINER.data_dirname = data_dirname
CONTAINER.data_filename = data_filename
CONTAINER.default_config = DefaultConfig
CONTAINER.entries = Entries
CONTAINER.entry_parser = EntryParser
CONTAINER.local_timezone = local_timezone
CONTAINER.now = now
CONTAINER.output = sys.stdout
CONTAINER.report = report
CONTAINER.timezone_config = timezone_config

for module in COMMAND_MODULES:
    setattr(CONTAINER, 'command/{}'.format(module.Command.NAME),
            module.Command.Handler)
