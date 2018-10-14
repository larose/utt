import datetime
from . import util


def now(args, timezone_config):
    if args.now:
        if timezone_config.enabled():
            return util.localize(args.now)

        return args.now

    now = datetime.datetime.today()
    if timezone_config.enabled():
        return util.localize(now)

    return now
