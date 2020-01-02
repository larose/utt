import datetime
import unittest

import ddt
import pytz

from utt.components.entry_parser import EntryParser

VALID_ENTRIES = [
    {
        "name": "2014-03-23 4:15 An activity",
        "expected_utc": datetime.datetime(2014, 3, 23, 4, 15),
        "expected_name": "An activity",
        "expected_comment": None,
        "tz": pytz.timezone("GMT"),
    },
    {
        "name": "2014-1-23   09:17   lunch**",
        "expected_utc": datetime.datetime(2014, 1, 23, 9, 17),
        "expected_name": "lunch**",
        "expected_comment": None,
        "tz": pytz.timezone("GMT"),
    },
    {
        "name": "2014-1-23  10:30+0930  travel",
        "expected_utc": datetime.datetime(2014, 1, 23, 1, 00),
        "expected_name": "travel",
        "expected_comment": None,
        "tz": pytz.timezone("Europe/London"),
    },
    {
        "name": "2014-1-23  10:30-0930 -work",
        "expected_utc": datetime.datetime(2014, 1, 23, 20, 00),
        "expected_name": "-work",
        "expected_comment": None,
        "tz": pytz.timezone("Singapore"),
    },
    {
        "name": "2014-1-23  10:30+01:00  break**",
        "expected_utc": datetime.datetime(2014, 1, 23, 9, 30),
        "expected_name": "break**",
        "expected_comment": None,
        "tz": pytz.timezone("US/Pacific"),
    },
    {
        "name": "2014-1-23  10:30-09:00  break**",
        "expected_utc": datetime.datetime(2014, 1, 23, 19, 30),
        "expected_name": "break**",
        "expected_comment": None,
        "tz": pytz.timezone("Australia/Sydney"),
    },
    {
        "name": "2014-1-23  10:30 -09:00  break**",
        "expected_utc": datetime.datetime(2014, 1, 22, 23, 30),
        "expected_name": "-09:00  break**",
        "expected_comment": None,
        "tz": pytz.timezone("Australia/Sydney"),
    },
    {
        "name": "2014-07-23  10:30  +work",  # daylight saving is on, UTC-04:00
        "expected_utc": datetime.datetime(2014, 7, 23, 14, 30),
        "expected_name": "+work",
        "expected_comment": None,
        "tz": pytz.timezone("US/Eastern"),
    },
    {
        "name": "2014-11-23  10:30  -work",  # daylight saving is off, UTC-05:00
        "expected_utc": datetime.datetime(2014, 11, 23, 15, 30),
        "expected_name": "-work",
        "expected_comment": None,
        "tz": pytz.timezone("US/Eastern"),
    },
    {
        "name": "2014-03-23 4:15 a-project: a_task",
        "expected_utc": datetime.datetime(2014, 3, 23, 4, 15),
        "expected_name": "a-project: a_task",
        "expected_comment": None,
        "tz": pytz.timezone("GMT"),
    },
    {
        "name": "2014-03-23 4:15 a-project: a_task  and something",
        "expected_utc": datetime.datetime(2014, 3, 23, 4, 15),
        "expected_name": "a-project: a_task  and something",
        "expected_comment": None,
        "tz": pytz.timezone("GMT"),
    },
    {
        "name": "2014-03-23 4:15 a-project: a_task  and something  # a comment",
        "expected_utc": datetime.datetime(2014, 3, 23, 4, 15),
        "expected_name": "a-project: a_task  and something",
        "expected_comment": "a comment",
        "tz": pytz.timezone("GMT"),
    },
]

INVALID_ENTRIES = [
    ("",),
    ("2014-",),
    ("2014-1-1",),
    ("9:15",),
    ("2015-1-1 9:15",),
    ("2014-03-23 An activity",),
]


@ddt.ddt
class ValidEntry(unittest.TestCase):
    @ddt.data(*VALID_ENTRIES)
    @ddt.unpack
    def test(self, name, expected_utc, expected_name, expected_comment, tz):
        entry_parser = EntryParser(tz)
        entry = entry_parser.parse(name)
        expected_datetime = tz.fromutc(expected_utc)
        self.assertEqual(entry.datetime, expected_datetime)
        self.assertEqual(entry.name, expected_name)
        self.assertEqual(entry.comment, expected_comment)


@ddt.ddt
class InvalidEntry(unittest.TestCase):
    @ddt.data(*INVALID_ENTRIES)
    @ddt.unpack
    def test(self, text):
        entry_parser = EntryParser(pytz.timezone("US/Pacific"))
        entry = entry_parser.parse(text)
        self.assertIsNone(entry)
