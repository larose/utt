import argparse
import typing

import tzlocal  # type: ignore
from pytz.tzinfo import DstTzInfo  # type: ignore

LocalTimezone = typing.NewType("LocalTimezone", DstTzInfo)  # type: ignore


def local_timezone(args: argparse.Namespace) -> LocalTimezone:
    if args.timezone:
        return LocalTimezone(args.timezone)

    return LocalTimezone(tzlocal.get_localzone())
