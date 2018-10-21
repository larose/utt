import calendar
import dateutil.tz
import time


def local_timezone(args, now):
    if args.timezone_offset:
        return args.timezone_offset

    local_time = time.localtime()
    offset_seconds = calendar.timegm(local_time) - \
        calendar.timegm(time.gmtime(time.mktime(local_time)))

    return dateutil.tz.tzoffset(None, offset_seconds)
