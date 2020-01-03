import argparse
import datetime
import typing

from .local_timezone import LocalTimezone

Now = typing.NewType("Now", datetime.datetime)


def now(args: argparse.Namespace, local_timezone: LocalTimezone) -> Now:
    if args.now:
        return Now(local_timezone.localize(args.now))

    return Now(local_timezone.localize(datetime.datetime.now()))
