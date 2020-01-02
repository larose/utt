import datetime


def now(args, local_timezone):
    if args.now:
        return local_timezone.localize(args.now)

    return local_timezone.localize(datetime.datetime.now())
