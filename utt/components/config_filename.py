import os

from ..constants import CONFIG_FILENAME


def config_filename(config_dirname: str) -> str:
    return os.path.join(config_dirname, CONFIG_FILENAME)
