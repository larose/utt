import argparse
import os

from ..constants import ENTRY_FILENAME


def data_filename(args: argparse.Namespace, data_dirname: str) -> str:
    if args.data_filename:
        return args.data_filename

    return os.path.join(data_dirname, ENTRY_FILENAME)
