from . import ioc
from .commands import command_modules
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

for module in command_modules:
    setattr(container, 'command/{}'.format(module.Command.NAME),
            module.Command.Handler)
