import os

from ..constants import DATA_HOME_DEFAULT_DIRNAME, DATA_HOME_ENV_VAR_NAME, DATA_HOME_SUB_DIRNAME


def data_dirname() -> str:
    base_data_dir_name = os.getenv(DATA_HOME_ENV_VAR_NAME, os.path.expanduser(DATA_HOME_DEFAULT_DIRNAME))

    return os.path.join(base_data_dir_name, DATA_HOME_SUB_DIRNAME)
