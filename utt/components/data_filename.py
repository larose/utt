import argparse
import os

from ..constants import ENTRY_FILENAME
from .data_dirname import DataDirname


class DataFilename(str):
    pass


def data_filename(args: argparse.Namespace, data_dirname: DataDirname) -> DataFilename:
    if args.data_filename:
        return args.data_filename

    return DataFilename(os.path.join(data_dirname, ENTRY_FILENAME))
