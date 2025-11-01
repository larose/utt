import datetime
import unittest

import ddt

from utt.components.entry_parser import EntryParser

VALID_ENTRIES = [
    {
        "name": "2014-03-23 4:15 An activity",
        "expected_datetime": datetime.datetime(2014, 3, 23, 4, 15),
        "expected_name": "An activity",
        "expected_comment": None,
    },
    {
        "name": "2014-1-23   09:17   lunch**",
        "expected_datetime": datetime.datetime(2014, 1, 23, 9, 17),
        "expected_name": "lunch**",
        "expected_comment": None,
    },
    {
        "name": "2014-07-23  10:30  +work",
        "expected_datetime": datetime.datetime(2014, 7, 23, 10, 30),
        "expected_name": "+work",
        "expected_comment": None,
    },
    {
        "name": "2014-11-23  10:30  -work",
        "expected_datetime": datetime.datetime(2014, 11, 23, 10, 30),
        "expected_name": "-work",
        "expected_comment": None,
    },
    {
        "name": "2014-03-23 4:15 a-project: a_task",
        "expected_datetime": datetime.datetime(2014, 3, 23, 4, 15),
        "expected_name": "a-project: a_task",
        "expected_comment": None,
    },
    {
        "name": "2014-03-23 4:15 a-project: a_task  and something",
        "expected_datetime": datetime.datetime(2014, 3, 23, 4, 15),
        "expected_name": "a-project: a_task  and something",
        "expected_comment": None,
    },
    {
        "name": "2014-03-23 4:15 a-project: a_task  and something  # a comment",
        "expected_datetime": datetime.datetime(2014, 3, 23, 4, 15),
        "expected_name": "a-project: a_task  and something",
        "expected_comment": "a comment",
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
    def test(self, name, expected_datetime, expected_name, expected_comment):
        entry_parser = EntryParser()
        entry = entry_parser.parse(name)
        self.assertEqual(entry.datetime, expected_datetime)
        self.assertEqual(entry.name, expected_name)
        self.assertEqual(entry.comment, expected_comment)


@ddt.ddt
class InvalidEntry(unittest.TestCase):
    @ddt.data(*INVALID_ENTRIES)
    @ddt.unpack
    def test(self, text):
        entry_parser = EntryParser()
        entry = entry_parser.parse(text)
        self.assertIsNone(entry)
