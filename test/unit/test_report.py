import datetime
import unittest

from utt.report.common import timedelta_to_billable

TEST_CASES = [
    (dict(minutes=0), " 0.0"),
    (dict(minutes=1), " 0.0"),
    (dict(minutes=2), " 0.0"),
    (dict(minutes=3), " 0.1"),
    (dict(minutes=4), " 0.1"),
    (dict(minutes=5), " 0.1"),
    (dict(minutes=6), " 0.1"),
    (dict(minutes=7), " 0.1"),
    (dict(minutes=8), " 0.1"),
    (dict(minutes=9), " 0.2"),
    (dict(minutes=14), " 0.2"),
    (dict(minutes=15), " 0.3"),
    (dict(minutes=30), " 0.5"),
    (dict(minutes=56), " 0.9"),
    (dict(minutes=57), " 1.0"),
    (dict(minutes=60), " 1.0"),
    (dict(minutes=62), " 1.0"),
    (dict(minutes=63), " 1.1"),
    (dict(minutes=66), " 1.1"),
    # NOTE, utt doesn't really deal with seconds, but this is how the
    #   rounding would work if it did.
    (dict(seconds=1), " 0.0"),
    (dict(seconds=179), " 0.0"),
    (dict(seconds=180), " 0.1"),
    (dict(seconds=181), " 0.1"),
    (dict(seconds=359), " 0.1"),
    (dict(seconds=360), " 0.1"),
    (dict(seconds=361), " 0.1"),
]


class TestTimedeltaToBillable(unittest.TestCase):
    def test_timedelta_to_billable(self):
        """Ensure that _timedelta_to_billable gives intended outcome.

        Hours are divided in 10, and we round up to the next "6 minute unit".
        """
        for delta, billable in TEST_CASES:
            with self.subTest(delta=delta, billable=billable):
                self.assertEqual(timedelta_to_billable(datetime.timedelta(**delta)), billable)
