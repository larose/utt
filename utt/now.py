import datetime


def now(args):
    if args.now:
        return args.now

    return datetime.datetime.now()
