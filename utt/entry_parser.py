import datetime
from .entry import Entry
from dateutil.parser import parse
import re

with_tz = re.compile(
    "(?P<date>\d{4}-\d{1,2}-\d{1,2}\s+\d{1,2}:\d{1,2})\s*(?P<timezone>[+-]{1}\d{2}:{0,1}\d{2})"
    "\s+(?P<name>[^\s].*)")

without_tz = re.compile(
    "(?P<date>\d{4}-\d{1,2}-\d{1,2}\s+\d{1,2}:\d{1,2})\s+(?P<name>[^\s].*)")


class EntryParser:
    def __init__(self, local_timezone):
        self._local_timezone = local_timezone

    def parse(self, string):
        match_wo_tz = without_tz.match(string)
        match_w_tz = with_tz.match(string)
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
            date = date.astimezone(self._local_timezone)
            date = date.replace(tzinfo=None)
        else:
            date = parse(date_str)

        name = match.groupdict()['name']
        return Entry(date, name, False)
