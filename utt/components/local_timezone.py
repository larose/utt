import argparse

import tzlocal
from pytz.tzinfo import DstTzInfo


def local_timezone(args: argparse.Namespace) -> DstTzInfo:
    if args.timezone:
        return args.timezone

    return tzlocal.get_localzone()
