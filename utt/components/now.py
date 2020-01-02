import argparse
import datetime

from pytz.tzinfo import DstTzInfo


def now(args: argparse.Namespace, local_timezone: DstTzInfo) -> datetime.datetime:
    if args.now:
        return local_timezone.localize(args.now)

    return local_timezone.localize(datetime.datetime.now())
