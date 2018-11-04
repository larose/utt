import sys


class ConfigHandler:
    def __init__(self, args, config, default_config, config_filename):
        self._args = args
        self._config = config
        self._default_config = default_config
        self._config_filename = config_filename

    def __call__(self):
        if self._args.filename:
            print(self._config_filename)
            return

        if self._args.default:
            self._default_config().write(sys.stdout)
            return

        self._config.write(sys.stdout)


class ConfigCommand:
    NAME = 'config'
    DESCRIPTION = 'Show config'

    Handler = ConfigHandler

    @staticmethod
    def add_args(parser):
        parser.add_argument("--default", action='store_true', default=False)
        parser.add_argument("--filename", action='store_true', default=False)


Command = ConfigCommand
