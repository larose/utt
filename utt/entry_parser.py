import re

from dateutil.parser import parse

from .entry import Entry

WITH_TZ = re.compile(
    r"(?P<date>\d{4}-\d{1,2}-\d{1,2}\s+\d{1,2}:\d{1,2})(?P<timezone>[+-]{1}\d{2}:{0,1}\d{2})"
    r"\s+(?P<name>[^\s].*)")

WITHOUT_TZ = re.compile(
    r"(?P<date>\d{4}-\d{1,2}-\d{1,2}\s+\d{1,2}:\d{1,2})\s+(?P<name>[^\s].*)")


class EntryParser:
    def __init__(self, local_timezone):
        self._local_timezone = local_timezone

    def parse(self, string):
        match_wo_tz = WITHOUT_TZ.match(string)
        match_w_tz = WITH_TZ.match(string)
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
        else:
            date = parse(date_str)
            date = self._local_timezone.localize(date)

        name = match.groupdict()['name']
        return Entry(date, name, False)
