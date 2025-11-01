import argparse
import datetime
import typing

Now = typing.NewType("Now", datetime.datetime)


def now(args: argparse.Namespace) -> Now:
    if args.now:
        return Now(args.now)

    return Now(datetime.datetime.now())
