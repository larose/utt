import datetime
import unittest

from utt.components.entries import UttError
from utt.components.report_args import parse_absolute_date, parse_absolute_month, parse_date

VALID_ENTRIES = [
    ("monday", datetime.date(2015, 2, 11), datetime.date(2015, 2, 9), True),
    ("tuesday", datetime.date(2015, 2, 11), datetime.date(2015, 2, 10), True),
    ("wednesday", datetime.date(2015, 2, 11), datetime.date(2015, 2, 11), True),
    ("thursday", datetime.date(2015, 2, 11), datetime.date(2015, 2, 5), True),
    ("friday", datetime.date(2015, 2, 11), datetime.date(2015, 2, 6), True),
    ("saturday", datetime.date(2015, 2, 11), datetime.date(2015, 2, 7), True),
    ("sunday", datetime.date(2015, 2, 11), datetime.date(2015, 2, 8), True),
    ("2015-2-8", datetime.date(2015, 2, 11), datetime.date(2015, 2, 8), True),
    ("monday", datetime.date(2015, 2, 11), datetime.date(2015, 2, 16), False),
    ("tuesday", datetime.date(2015, 2, 11), datetime.date(2015, 2, 17), False),
    ("wednesday", datetime.date(2015, 2, 11), datetime.date(2015, 2, 11), False),
    ("thursday", datetime.date(2015, 2, 11), datetime.date(2015, 2, 12), False),
    ("friday", datetime.date(2015, 2, 11), datetime.date(2015, 2, 13), False),
    ("saturday", datetime.date(2015, 2, 11), datetime.date(2015, 2, 14), False),
    ("sunday", datetime.date(2015, 2, 11), datetime.date(2015, 2, 15), False),
]


class ParseDate(unittest.TestCase):
    def test_parse_date(self):
        for test_case in VALID_ENTRIES:
            report_date, today, expected_report_date, is_past = test_case
            with self.subTest(report_date=report_date, today=today, is_past=is_past):
                actual_report_date = parse_date(today, report_date, is_past)
                self.assertEqual(actual_report_date, expected_report_date)

    def test_invalid_date_raises_utt_error(self):
        with self.assertRaises(UttError):
            parse_absolute_date("invalid-date")

    def test_invalid_month_raises_utt_error(self):
        with self.assertRaises(UttError):
            parse_absolute_month("invalid-month")

    def test_valid_absolute_date(self):
        result = parse_absolute_date("2024-01-15")
        self.assertEqual(result, datetime.date(2024, 1, 15))

    def test_valid_absolute_month(self):
        result = parse_absolute_month("2024-01")
        self.assertEqual(result, datetime.date(2024, 1, 1))
