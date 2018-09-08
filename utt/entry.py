import datetime
import re

from dateutil.parser import parse
import pytz
from .util import localize


class Entry:
    with_tz = re.compile(
        "(?P<date>\d{4}-\d{1,2}-\d{1,2}\s+\d{1,2}:\d{1,2})\s*(?P<timezone>[+-]{1}\d{2}:{0,1}\d{2})"
        "\s+(?P<name>[^\s].*)")
    without_tz = re.compile(
        "(?P<date>\d{4}-\d{1,2}-\d{1,2}\s+\d{1,2}:\d{1,2})\s+(?P<name>[^\s].*)")

    def __init__(self, datetime, name, is_current_entry):
        self.datetime = datetime
        self.name = name
        self.is_current_entry = is_current_entry

    def __str__(self):
        return " ".join(
            [self.datetime.strftime("%Y-%m-%d %H:%M%z"), self.name])

    @staticmethod
    def from_string(string):
        match_wo_tz = Entry.without_tz.match(string)
        match_w_tz = Entry.with_tz.match(string)
        match = match_w_tz if match_w_tz is not None else match_wo_tz

        if match is None:
            return None

        groupdict = match.groupdict()

        if 'date' not in groupdict or 'name' not in groupdict:
            return None

        date_str = groupdict['date']
        if 'timezone' in groupdict:
            date_str += groupdict['timezone'].replace(':', '')

        date = parse(date_str)

        if date.utcoffset() is None:
            try:
                date = localize(date)
            except pytz.InvalidTimeError as exc:
                exc_cls = type(exc)
                raise exc_cls(
                    "{!r} is not a valid time for the local time zone.".format(
                        date_str))

        name = match.groupdict()['name']
        return Entry(date, name, False)
