import datetime
import ddt
import unittest

from utt.cmd_report import _fetch_entries_of_day
from utt.entry import Entry

TOUCHING_NEXT_DAY_REPORT_DAY = datetime.datetime.strptime("2014-03-23", "%Y-%m-%d")
TOUCHING_NEXT_DAY = {
    TOUCHING_NEXT_DAY_REPORT_DAY: [
        Entry.from_string("2014-03-23 17:00 hello"),
        Entry.from_string("2014-03-23 23:15 An activity")
    ],
    TOUCHING_NEXT_DAY_REPORT_DAY + datetime.timedelta(days=1): [
        Entry.from_string("2014-03-24 0:15 Another activity"),
        Entry.from_string("2014-03-24 3:05 Finish last test")
    ]
}


VALID_ENTRIES = [
    {
        'raw_entries': TOUCHING_NEXT_DAY,
        'report_date': TOUCHING_NEXT_DAY_REPORT_DAY,

        'expected': [
            Entry.from_string("2014-03-23 17:00 hello"),
            Entry.from_string("2014-03-23 23:15 An activity"),
            Entry.from_string("2014-03-23 23:59 Another activity (finishes a day later)")
        ]
    },
    {
        'raw_entries': TOUCHING_NEXT_DAY,
        'report_date': TOUCHING_NEXT_DAY_REPORT_DAY + datetime.timedelta(days=1),

        'expected': [
            Entry.from_string("2014-03-24 00:00 An activity (started the day before)"),
            Entry.from_string("2014-03-24 0:15 Another activity"),
            Entry.from_string("2014-03-24 3:05 Finish last test")
        ]
    }
]


@ddt.ddt
class ValidEntry(unittest.TestCase):
    @ddt.data(*VALID_ENTRIES)
    @ddt.unpack
    def test(self, raw_entries, report_date, expected):
        entries = _fetch_entries_of_day(raw_entries, report_date)
        self.assertEqual(len(entries), len(expected))
        self.assertEqual(len(entries), 3)
        self.assertEqual(entries[0], expected[0])
        self.assertEqual(entries[1], expected[1])

    @ddt.data(VALID_ENTRIES[0])
    @ddt.unpack
    def test2(self, raw_entries, report_date, expected):
        entries = _fetch_entries_of_day(raw_entries, report_date)
        last_entry = Entry.from_string(str(entries[2]))
        last_entry.datetime = last_entry.datetime.replace(hour=23, minute=59)
        last_entry.name += " (finishes a day later)"
        self.assertEqual(entries[2], expected[2])

    @ddt.data(VALID_ENTRIES[1])
    @ddt.unpack
    def test3(self, raw_entries, report_date, expected):
        entries = _fetch_entries_of_day(raw_entries, report_date)
        last_entry = Entry.from_string(str(entries[2]))
        last_entry.datetime = last_entry.datetime.replace(hour=0, minute=0)
        last_entry.name += " (started the day before)"
        self.assertEqual(entries[2], expected[2])
