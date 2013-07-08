import datetime
import collections
import errno
import os
import re

Entry = collections.namedtuple('Entry', ['datetime', 'activity'])

def add_entry(filename, entry):
    last_entry = _last_element(entries(filename))

    if last_entry and entry.datetime < last_entry.datetime:
        raise Exception("Now less than last entry: %s < %s" % 
                        (entry.datetime, last_entry.datetime))

    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
    except OSError as exc:
        # We called os.makedirs with exist_ok=True so if the exception
        # is errno.EEXIST, then it's a mode issue. We ignore it
        # because it doesn't imply that the user has no permission
        # (e.g. sticky bit on /tmp).
        if exc.errno != errno.EEXIST:
            raise

    with open(filename, 'a') as file:
        file.write(" ".join([_format_datetime(entry.datetime),
                             entry.activity]) + "\n")

def entries(filename):
    try:
        return _parse_data(open(filename))
    except IOError as ex:
        if ex.errno == errno.ENOENT:
            return [Entry(datetime.datetime(1970, 1, 1), '')]
        raise

_entry_regex = re.compile(
    "(?P<date>\d{4}-\d{1,2}-\d{1,2}\s+\d{1,2}:\d{1,2})\s+(?P<entry>[^\s].*)")

def _format_datetime(datetime):
    return datetime.strftime("%Y-%m-%d %H:%M")

def _last_element(sequence):
    deque = collections.deque(sequence, maxlen=1)
    if deque:
        return deque.pop()

def _parse_data(data):
    previous_date = None
    for i, line in enumerate(filter(lambda line: line.strip(), data), 1):
        entry = _parse_line(line)

        if entry is None:
            raise Exception("Invalid syntax at line %d: %s" % (i, line))

        if previous_date and previous_date > entry.datetime:
            raise Exception(
                "Error line %d. Not in chronological order: %s > %s" % 
                (i, previous_date, entry.datetime))
        previous_date = entry.datetime
        yield entry

def _parse_datetime(string):
    return datetime.datetime.strptime(string, "%Y-%m-%d %H:%M")

def _parse_line(line):
    match = _entry_regex.match(line.strip())

    if match is None:
        return None

    groupdict = match.groupdict()

    if 'date' not in groupdict or 'entry' not in groupdict:
        return None

    date = _parse_datetime(groupdict['date'])
    entry = match.groupdict()['entry']
    return Entry(date, entry)
