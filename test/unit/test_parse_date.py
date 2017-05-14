import datetime
import ddt
import unittest
from utt.cmd_report import _parse_date

VALID_ENTRIES = [
    ("monday", datetime.datetime(2015, 2, 11, 7, 0), datetime.date(2015, 2,
                                                                   9)),
    ("tuesday", datetime.datetime(2015, 2, 11, 7, 0), datetime.date(
        2015, 2, 10)),
    ("wednesday", datetime.datetime(2015, 2, 11, 7, 0), datetime.date(
        2015, 2, 11)),
    ("thursday", datetime.datetime(2015, 2, 11, 7, 0), datetime.date(
        2015, 2, 5)),
    ("friday", datetime.datetime(2015, 2, 11, 7, 0), datetime.date(2015, 2,
                                                                   6)),
    ("saturday", datetime.datetime(2015, 2, 11, 7, 0), datetime.date(
        2015, 2, 7)),
    ("sunday", datetime.datetime(2015, 2, 11, 7, 0), datetime.date(2015, 2,
                                                                   8)),
    ("2015-2-8", datetime.datetime(2015, 2, 11, 7, 0), datetime.date(
        2015, 2, 8)),
]


@ddt.ddt
class ParseDate(unittest.TestCase):
    @ddt.data(*VALID_ENTRIES)
    @ddt.unpack
    def test(self, report_date, now, expected_report_date):
        actual_report_date = _parse_date(now, report_date)
        self.assertEqual(actual_report_date, expected_report_date)
