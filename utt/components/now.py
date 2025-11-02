import argparse
import datetime


class Now(datetime.datetime):
    pass


def now(args: argparse.Namespace) -> Now:
    if args.now:
        return Now.fromtimestamp(args.now.timestamp())

    dt = datetime.datetime.now()
    return Now.fromtimestamp(dt.timestamp())
