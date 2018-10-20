import datetime
from . import util


def now(args, timezone_config):
    if args.now:
        return args.now

    return datetime.datetime.today()
