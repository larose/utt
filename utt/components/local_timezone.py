import argparse
import typing

import tzlocal
from pytz.tzinfo import DstTzInfo

LocalTimezone = typing.NewType("LocalTimezone", DstTzInfo)


def local_timezone(args: argparse.Namespace) -> LocalTimezone:
    if args.timezone:
        return LocalTimezone(args.timezone)

    return LocalTimezone(tzlocal.get_localzone())
