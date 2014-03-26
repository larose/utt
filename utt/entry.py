import datetime
import re

class Entry:
    regex = re.compile(
        "(?P<date>\d{4}-\d{1,2}-\d{1,2}\s+\d{1,2}:\d{1,2})\s+(?P<name>[^\s].*)"
        )

    def __init__(self, datetime, name, is_current_entry):
        self.datetime = datetime
        self.name = name
        self.is_current_entry = is_current_entry

    def __str__(self):
        return " ".join([self.datetime.strftime("%Y-%m-%d %H:%M"),
                         self.name])

    @staticmethod
    def from_string(string):
        match = Entry.regex.match(string)

        if match is None:
            return None

        groupdict = match.groupdict()

        if 'date' not in groupdict or 'name' not in groupdict:
            return None

        date = datetime.datetime.strptime(groupdict['date'], "%Y-%m-%d %H:%M")
        name = match.groupdict()['name']
        return Entry(date, name, False)
