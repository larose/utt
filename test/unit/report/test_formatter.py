import unittest
from datetime import timedelta

from utt.report.formatter import format_duration


class TestFormatter(unittest.TestCase):
    def test_formatter_less_than_a_minute(self):
        self.assertEqual(format_duration(timedelta(seconds=10)), "0h00")

    def test_formatter_less_than_a_hour(self):
        self.assertEqual(format_duration(timedelta(minutes=8, seconds=45)), "0h08")

    def test_formatter_less_than_a_day(self):
        self.assertEqual(format_duration(timedelta(hours=8, minutes=20)), "8h20")

    def test_formatter_more_than_a_day(self):
        self.assertEqual(format_duration(timedelta(days=1, hours=2, minutes=20)), "26h20")
