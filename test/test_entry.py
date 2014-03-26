import datetime
import ddt
import unittest
from utt.entry import Entry

VALID_ENTRIES = [
    {
        'name': "2014-03-23 4:15 An activity",
        'expected_datetime': datetime.datetime(2014, 3, 23, 4, 15),
        'expected_name': "An activity"
    },
    {
        'name': "2014-1-23   09:17   lunch**",
        'expected_datetime': datetime.datetime(2014, 1, 23, 9, 17),
        'expected_name': "lunch**"
    }
]

INVALID_ENTRIES = [
    ("",),
    ("2014-",),
    ("2014-1-1",),
    ("9:15",),
    ("2015-1-1 9:15",),
    ("2014-03-23 An activity",)
]

@ddt.ddt
class ValidEntry(unittest.TestCase):
    @ddt.data(*VALID_ENTRIES)
    @ddt.unpack
    def test(self, name, expected_datetime, expected_name):
        entry = Entry.from_string(name)
        self.assertEqual(entry.datetime, expected_datetime)
        self.assertEqual(entry.name, expected_name)

@ddt.ddt
class InvalidEntry(unittest.TestCase):
    @ddt.data(*INVALID_ENTRIES)
    @ddt.unpack
    def test(self, text):
        entry = Entry.from_string(text)
        self.assertIsNone(entry)
