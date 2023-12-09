import argparse
import typing

import pytz
import tzlocal
from pytz.tzinfo import DstTzInfo

LocalTimezone = typing.NewType("LocalTimezone", DstTzInfo)


def local_timezone(args: argparse.Namespace) -> LocalTimezone:
    if args.timezone:
        return LocalTimezone(args.timezone)

    return LocalTimezone(pytz.timezone(tzlocal.get_localzone_name()))
