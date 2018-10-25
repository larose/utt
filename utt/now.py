import datetime


def now(args, timezone_config):
    if args.now:
        return args.now

    return datetime.datetime.now()
