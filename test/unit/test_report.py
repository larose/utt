# pylint: disable=redefined-outer-name

import datetime

import pytest
import pytz

import utt.report
from utt.activities import Activities
from utt.entry import Entry


class Args:
    # pylint: disable=too-many-instance-attributes
    def __init__(self):
        self.current_activity = "-- Current Activity --"
        self.from_date = None
        self.no_current_activity = False
        self.report_date = None
        self.to_date = None
        self.project = None
        self.per_day = None
        self.month = None
        self.week = None


class InMemoryEntries:
    def __init__(self, entries):
        self._entries = entries

    def __call__(self):
        return self._entries


@pytest.fixture()
def args():
    return Args()


@pytest.fixture()
def local_timezone():
    return pytz.timezone('America/Montreal')


@pytest.fixture()
def entries(local_timezone):
    entry_list = [
        Entry(datetime.datetime(2014, 3, 14, 8, 0), "hello", False),
        Entry(datetime.datetime(2014, 3, 14, 9, 0), "hard work", False),
        Entry(datetime.datetime(2014, 3, 17, 9, 0), "hello", False),
        Entry(datetime.datetime(2014, 3, 17, 10, 15), "hard work", False),
        Entry(datetime.datetime(2014, 3, 19, 9, 0), "hello", False),
        Entry(datetime.datetime(2014, 3, 19, 12, 0), "asd: A-526", False),
        Entry(datetime.datetime(2014, 3, 19, 13, 0), "lunch**", False),
        Entry(datetime.datetime(2014, 3, 19, 14, 0), "hard work", False),
        Entry(datetime.datetime(2014, 3, 19, 14, 15), "qwer: b-73", False),
        Entry(datetime.datetime(2014, 3, 19, 14, 30), "asd: A-526", False),
        Entry(datetime.datetime(2014, 3, 19, 14, 45), "qwer: C-123", False),
        Entry(datetime.datetime(2014, 3, 19, 15, 0), "qwer: a-9", False),
        Entry(datetime.datetime(2014, 3, 19, 16, 0), "black out ***", False),
        Entry(datetime.datetime(2014, 3, 19, 16, 30), "A: z-8", False),
    ]

    for entry in entry_list:
        entry.datetime = local_timezone.localize(entry.datetime)

    return InMemoryEntries(entry_list)


@pytest.fixture()
def activities(entries):
    return Activities(entries)


def test_range(args, activities, local_timezone):
    now = local_timezone.localize(datetime.datetime(2014, 3, 19, 18, 30))

    args.from_date = "2014-03-15"
    args.to_date = "2014-03-19"
    args.no_current_activity = True

    actual_report = utt.report.report(args, now, activities, local_timezone)
    assert actual_report.summary_model.working_time.total_duration == datetime.timedelta(
        hours=6, minutes=45)
    assert actual_report.summary_model.working_time.weekly_duration == datetime.timedelta(
        hours=6, minutes=45)
    assert actual_report.summary_model.break_time.weekly_duration == datetime.timedelta(
        hours=1)
    assert actual_report.summary_model.break_time.weekly_duration == datetime.timedelta(
        hours=1)


def test_weekday_range(args, activities, local_timezone):
    now = local_timezone.localize(datetime.datetime(2014, 3, 19, 18, 30))

    args.from_date = "tuesday"  # 2014-03-18
    args.to_date = "wednesday"  # 2014-03-19
    args.no_current_activity = True

    actual_report = utt.report.report(args, now, activities, local_timezone)
    assert actual_report.summary_model.working_time.total_duration == datetime.timedelta(
        hours=5, minutes=30)
    assert actual_report.summary_model.working_time.weekly_duration == datetime.timedelta(
        hours=5, minutes=30)
    assert actual_report.summary_model.break_time.weekly_duration == datetime.timedelta(
        hours=1)
    assert actual_report.summary_model.break_time.weekly_duration == datetime.timedelta(
        hours=1)


def test_single_day(args, activities, local_timezone):
    now = local_timezone.localize(datetime.datetime(2014, 3, 19, 18, 30))

    actual_report = utt.report.report(args, now, activities, local_timezone)
    assert actual_report.summary_model.working_time.total_duration == datetime.timedelta(
        hours=7, minutes=30)
    assert actual_report.summary_model.working_time.weekly_duration == datetime.timedelta(
        hours=8, minutes=45)
    assert actual_report.summary_model.break_time.weekly_duration == datetime.timedelta(
        hours=1)
    assert actual_report.summary_model.break_time.weekly_duration == datetime.timedelta(
        hours=1)


@pytest.mark.parametrize(
    "delta,billable",
    [
        (dict(minutes=0), ' 0.0'),
        (dict(minutes=1), ' 0.0'),
        (dict(minutes=2), ' 0.0'),
        (dict(minutes=3), ' 0.1'),
        (dict(minutes=4), ' 0.1'),
        (dict(minutes=5), ' 0.1'),
        (dict(minutes=6), ' 0.1'),
        (dict(minutes=7), ' 0.1'),
        (dict(minutes=8), ' 0.1'),
        (dict(minutes=9), ' 0.2'),
        (dict(minutes=14), ' 0.2'),
        (dict(minutes=15), ' 0.3'),
        (dict(minutes=30), ' 0.5'),
        (dict(minutes=56), ' 0.9'),
        (dict(minutes=57), ' 1.0'),
        (dict(minutes=60), ' 1.0'),
        (dict(minutes=62), ' 1.0'),
        (dict(minutes=63), ' 1.1'),
        (dict(minutes=66), ' 1.1'),
        # NOTE, utt doesn't really deal with seconds, but this is how the
        #   rounding would work if it did.
        (dict(seconds=1), ' 0.0'),
        (dict(seconds=179), ' 0.0'),
        (dict(seconds=180), ' 0.1'),
        (dict(seconds=181), ' 0.1'),
        (dict(seconds=359), ' 0.1'),
        (dict(seconds=360), ' 0.1'),
        (dict(seconds=361), ' 0.1'),
    ])
def test_timedelta_to_billable(delta, billable):
    """Ensure that _timedelta_to_billable gives intended outcome.

    Hours are divided in 10, and we round up to the next "6 minute unit".
    """
    # pylint: disable=protected-access
    to_billable = utt.report.per_day_section.PerDayView._timedelta_to_billable
    assert to_billable(datetime.timedelta(**delta)) == billable
