# pylint: disable=invalid-name
def format_duration(duration):
    mm, _ = divmod(duration.seconds, 60)
    hh, mm = divmod(mm, 60)
    s = "%dh%02d" % (hh, mm)
    if duration.days:

        def plural(n):
            return n, abs(n) != 1 and "s" or ""

        s = ("%d day%s, " % plural(duration.days)) + s
    return s


def title(text):
    return '{:-^80}'.format(' ' + text + ' ')
