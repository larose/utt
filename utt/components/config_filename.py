import os
import typing

from ..constants import CONFIG_FILENAME
from .config_dirname import ConfigDirname

ConfigFilename = typing.NewType("ConfigFilename", str)


def config_filename(config_dirname: ConfigDirname) -> ConfigFilename:
    return ConfigFilename(os.path.join(config_dirname, CONFIG_FILENAME))
