import os
import typing

from ..constants import DATA_HOME_DEFAULT_DIRNAME, DATA_HOME_ENV_VAR_NAME, DATA_HOME_SUB_DIRNAME

DataDirname = typing.NewType("DataDirname", str)


def data_dirname() -> DataDirname:
    base_data_dir_name = os.getenv(DATA_HOME_ENV_VAR_NAME, os.path.expanduser(DATA_HOME_DEFAULT_DIRNAME))

    return DataDirname(os.path.join(base_data_dir_name, DATA_HOME_SUB_DIRNAME))
