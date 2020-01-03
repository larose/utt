import configparser

from .config_filename import ConfigFilename
from .default_config import DefaultConfig


def config(config_filename: ConfigFilename, default_config: DefaultConfig) -> configparser.ConfigParser:
    conf = default_config()
    conf.read(config_filename)
    return conf
