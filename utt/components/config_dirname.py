import os

from ..constants import DATA_CONFIG_DEFAULT_DIRNAME, DATA_CONFIG_ENV_VAR_NAME, DATA_CONFIG_SUB_DIRNAME


class ConfigDirname(str):
    pass


def config_dirname() -> ConfigDirname:
    base_dir_name = os.getenv(DATA_CONFIG_ENV_VAR_NAME, os.path.expanduser(DATA_CONFIG_DEFAULT_DIRNAME))

    return ConfigDirname(os.path.join(base_dir_name, DATA_CONFIG_SUB_DIRNAME))
