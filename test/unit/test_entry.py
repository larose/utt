import datetime
import ddt
import pytz
import unittest
try:
    from unittest import mock
except ImportError:
    import mock
from utt.entry import Entry

VALID_ENTRIES = [
    {
        'name': "2014-03-23 4:15 An activity",
        'expected_utc': datetime.datetime(2014, 3, 23, 4, 15),
        'expected_name': "An activity",
        'tz': pytz.timezone("GMT"),
    },
    {
        'name': "2014-1-23   09:17   lunch**",
        'expected_utc': datetime.datetime(2014, 1, 23, 9, 17),
        'expected_name': "lunch**",
        'tz': pytz.timezone("GMT"),
    },
    {
        'name': "2014-1-23  10:30+0930  travel",
        'expected_utc': datetime.datetime(2014, 1, 23, 1, 00),
        'expected_name': "travel",
        'tz': pytz.timezone("Europe/London"),
    },
    {
        'name': "2014-1-23  10:30-0930 -work",
        'expected_utc': datetime.datetime(2014, 1, 23, 20, 00),
        'expected_name': "-work",
        'tz': pytz.timezone("Singapore"),
    },
    {
        'name': "2014-1-23  10:30+01:00  break**",
        'expected_utc': datetime.datetime(2014, 1, 23, 9, 30),
        'expected_name': "break**",
        'tz': pytz.timezone("US/Pacific"),
    },
    {
        'name': "2014-1-23  10:30  -09:00  break**",
        'expected_utc': datetime.datetime(2014, 1, 23, 19, 30),
        'expected_name': "break**",
        'tz': pytz.timezone("Australia/Sydney"),
    },
    {
        'name': "2014-07-23  10:30  +work",  # daylight saving is on, UTC-04:00
        'expected_utc': datetime.datetime(2014, 7, 23, 14, 30),
        'expected_name': "+work",
        'tz': pytz.timezone("US/Eastern"),
    },
    {
        'name':
        "2014-11-23  10:30  -work",  # daylight saving is off, UTC-05:00
        'expected_utc': datetime.datetime(2014, 11, 23, 15, 30),
        'expected_name': "-work",
        'tz': pytz.timezone("US/Eastern"),
    }
]

INVALID_ENTRIES = [("", ), ("2014-", ), ("2014-1-1", ), ("9:15", ),
                   ("2015-1-1 9:15", ), ("2014-03-23 An activity", )]


@ddt.ddt
class ValidEntry(unittest.TestCase):
    @ddt.data(*VALID_ENTRIES)
    @ddt.unpack
    def test(self, name, expected_utc, expected_name, tz):
        with mock.patch("tzlocal.get_localzone", return_value=tz):
            entry = Entry.from_string(name)
        expected_datetime = tz.fromutc(expected_utc)
        self.assertEqual(entry.datetime, expected_datetime)
        self.assertEqual(entry.name, expected_name)

    def test_invalid_time(self):
        tz = pytz.timezone("US/Eastern")
        entry_str = "2002-04-07 02:30 practice"
        with self.assertRaises(pytz.NonExistentTimeError) as exc_cm:
            with mock.patch("tzlocal.get_localzone", return_value=tz):
                Entry.from_string(entry_str)

        # The user should be notified which entry is problematic
        # then they can fix it with a timezone offset
        self.assertEqual(
            str(exc_cm.exception),
            "'2002-04-07 02:30' is not a valid time for the local time zone.")


@ddt.ddt
class InvalidEntry(unittest.TestCase):
    @ddt.data(*INVALID_ENTRIES)
    @ddt.unpack
    def test(self, text):
        entry = Entry.from_string(text)
        self.assertIsNone(entry)
