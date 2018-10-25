import sys

from . import ioc
from . import commands
from .entry_parser import EntryParser
from .data_dirname import data_dirname
from .data_filename import data_filename
from .log_repo import LogRepo
from .now import now
from .timezone_config import timezone_config
from .local_timezone import local_timezone
from .config_dirname import config_dirname
from .config_filename import config_filename
from .config import config
from .default_config import DefaultConfig
from .parse_args import parse_args

COMMAND_MODULES = [
    commands.add, commands.config, commands.edit, commands.hello,
    commands.stretch, commands.report
]


def main():
    if len(sys.argv) == 1:
        sys.argv.append('--help')

    container = ioc.Container()
    container.args = parse_args
    container.config = config
    container.config_dirname = config_dirname
    container.config_filename = config_filename
    container.data_dirname = data_dirname
    container.data_filename = data_filename
    container.default_config = DefaultConfig
    container.entry_parser = EntryParser
    container.now = now
    container.local_timezone = local_timezone
    container.log_repo = LogRepo
    container.timezone_config = timezone_config

    for module in COMMAND_MODULES:
        setattr(container, 'command/{}'.format(module.Command.NAME),
                module.Command.Handler)

    getattr(container, 'command/{}'.format(container.args.command))()


if __name__ == '__main__':
    main()
