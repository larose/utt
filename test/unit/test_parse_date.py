import datetime
import unittest

import ddt

from utt.report import _parse_date

VALID_ENTRIES = [
    ("monday", datetime.date(2015, 2, 11), datetime.date(2015, 2, 9), True),
    ("tuesday", datetime.date(2015, 2, 11), datetime.date(2015, 2, 10), True),
    ("wednesday", datetime.date(2015, 2, 11), datetime.date(2015, 2, 11),
     True),
    ("thursday", datetime.date(2015, 2, 11), datetime.date(2015, 2, 5), True),
    ("friday", datetime.date(2015, 2, 11), datetime.date(2015, 2, 6), True),
    ("saturday", datetime.date(2015, 2, 11), datetime.date(2015, 2, 7), True),
    ("sunday", datetime.date(2015, 2, 11), datetime.date(2015, 2, 8), True),
    ("2015-2-8", datetime.date(2015, 2, 11), datetime.date(2015, 2, 8), True),
    ("monday", datetime.date(2015, 2, 11), datetime.date(2015, 2, 16), False),
    ("tuesday", datetime.date(2015, 2, 11), datetime.date(2015, 2, 17), False),
    ("wednesday", datetime.date(2015, 2, 11), datetime.date(2015, 2, 11),
     False),
    ("thursday", datetime.date(2015, 2, 11), datetime.date(2015, 2, 12),
     False),
    ("friday", datetime.date(2015, 2, 11), datetime.date(2015, 2, 13), False),
    ("saturday", datetime.date(2015, 2, 11), datetime.date(2015, 2, 14),
     False),
    ("sunday", datetime.date(2015, 2, 11), datetime.date(2015, 2, 15), False),
]


@ddt.ddt
class ParseDate(unittest.TestCase):
    @ddt.data(*VALID_ENTRIES)
    @ddt.unpack
    def test(self, report_date, today, expected_report_date, is_past):
        actual_report_date = _parse_date(today, report_date, is_past)
        self.assertEqual(actual_report_date, expected_report_date)
