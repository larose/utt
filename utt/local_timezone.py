import tzlocal

def local_timezone(args):
    if args.timezone_offset:
        return args.timezone_offset

    return tzlocal.get_localzone()
