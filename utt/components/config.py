import configparser

from .default_config import DefaultConfig


def config(config_filename: str, default_config: DefaultConfig) -> configparser.ConfigParser:
    conf = default_config()
    conf.read(config_filename)
    return conf
