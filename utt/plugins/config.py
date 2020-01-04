import argparse
import configparser
import sys

from ..api import _v1
from ..command import Command
from ..components.config_filename import ConfigFilename  # Private API
from ..components.default_config import DefaultConfig  # Private API


class ConfigHandler:
    def __init__(
        self,
        args: argparse.Namespace,
        config: configparser.ConfigParser,
        default_config: DefaultConfig,
        config_filename: ConfigFilename,
    ):
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


def add_args(parser: argparse.ArgumentParser):
    parser.add_argument("--default", action="store_true", default=False)
    parser.add_argument("--filename", action="store_true", default=False)


config_command = Command("config", "Show config", ConfigHandler, add_args)


_v1.add_command(config_command)
