import sys


class ConfigHandler:
    def __init__(self, args, config, default_config):
        self._args = args
        self._config = config
        self._default_config = default_config

    def __call__(self):
        if self._args.default:
            self._default_config().write(sys.stdout)
        else:
            self._config.write(sys.stdout)


class ConfigCommand:
    NAME = 'config'
    DESCRIPTION = 'Show config'

    Handler = ConfigHandler

    @staticmethod
    def add_args(parser):
        parser.add_argument("--default", action='store_true', default=False)


Command = ConfigCommand
