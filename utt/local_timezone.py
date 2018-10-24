import calendar
import dateutil.tz
import time
import tzlocal


def local_timezone(args, now):
    if args.timezone:
        return args.timezone

    return tzlocal.get_localzone()
