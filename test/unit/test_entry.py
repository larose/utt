import datetime
import unittest

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
    ("2025-27-27 17:00 misc: testing",),
]


class ValidEntry(unittest.TestCase):
    def test_valid_entries(self):
        for test_case in VALID_ENTRIES:
            with self.subTest(name=test_case["name"]):
                entry_parser = EntryParser()
                entry = entry_parser.parse(test_case["name"])

                self.assertEqual(entry.datetime, test_case["expected_datetime"])
                self.assertEqual(entry.name, test_case["expected_name"])
                self.assertEqual(entry.comment, test_case["expected_comment"])


class InvalidEntry(unittest.TestCase):
    def test_invalid_entries_raise_value_error(self):
        """Test that invalid entries raise ValueError."""
        for test_case in INVALID_ENTRIES:
            with self.subTest(text=test_case[0]):
                entry_parser = EntryParser()
                with self.assertRaises(ValueError):
                    entry_parser.parse(test_case[0])

