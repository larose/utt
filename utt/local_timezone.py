import tzlocal


def local_timezone(args):
    if args.timezone:
        return args.timezone

    return tzlocal.get_localzone()
