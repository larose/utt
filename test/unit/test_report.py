# pylint: disable=redefined-outer-name

import datetime
import io

import pytest

from utt.commands.report import ReportHandler
from utt.entry import Entry
from utt.activities import Activities


class Args:
    def __init__(self):
        self.current_activity = "-- Current Activity --"
        self.from_date = None
        self.no_current_activity = False
        self.report_date = None
        self.to_date = None


class InMemoryEntries:
    def __init__(self, entries):
        self._entries = entries

    def __call__(self):
        return self._entries


@pytest.fixture
def expected_output_single_day():
    return """
---------------------- Wednesday, Mar 19, 2014 (week 12) -----------------------

Working Time: 7h30 (5h30 + 2h00) [8h45]
Break   Time: 1h00 [1h00]

----------------------------------- Projects -----------------------------------

(3h00)     : -- Current Activity --, hard work
(0h30) A   : z-8
(3h15) asd : A-526
(0h45) qwer: a-9, b-73, C-123

---------------------------------- Activities ----------------------------------

(2h00)     : -- Current Activity --
(1h00)     : hard work
(0h30) A   : z-8
(3h15) asd : A-526
(0h15) qwer: a-9
(0h15) qwer: b-73
(0h15) qwer: C-123

(1h00) : lunch**

----------------------------------- Details ------------------------------------

(3h00) 09:00-12:00 asd: A-526
(1h00) 12:00-13:00 lunch**
(1h00) 13:00-14:00 hard work
(0h15) 14:00-14:15 qwer: b-73
(0h15) 14:15-14:30 asd: A-526
(0h15) 14:30-14:45 qwer: C-123
(0h15) 14:45-15:00 qwer: a-9
(1h00) 15:00-16:00 black out ***
(0h30) 16:00-16:30 A: z-8
(2h00) 16:30-18:30 -- Current Activity --

"""


@pytest.fixture
def expected_output_range():
    return """
---- Saturday, Mar 15, 2014 (week 11) to Wednesday, Mar 19, 2014 (week 12) -----

Working Time: 6h45
Break   Time: 1h00

----------------------------------- Projects -----------------------------------

(2h15)     : hard work
(0h30) A   : z-8
(3h15) asd : A-526
(0h45) qwer: a-9, b-73, C-123

---------------------------------- Activities ----------------------------------

(2h15)     : hard work
(0h30) A   : z-8
(3h15) asd : A-526
(0h15) qwer: a-9
(0h15) qwer: b-73
(0h15) qwer: C-123

(1h00) : lunch**
"""


@pytest.fixture()
def args():
    return Args()


@pytest.fixture()
def entries():
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

    return InMemoryEntries(entry_list)


@pytest.fixture()
def activities(entries):
    return Activities(entries)


def test_range(args, activities, expected_output_range):
    now = datetime.datetime(2014, 3, 19, 18, 30)

    args.from_date = datetime.date(2014, 3, 15)
    args.to_date = datetime.date(2014, 3, 19)
    args.no_current_activity = True

    actual_output = io.StringIO()
    report_handler = ReportHandler(args, now, activities)
    report_handler.output = actual_output
    report_handler()
    assert expected_output_range == actual_output.getvalue()


def test_single_day(args, activities, expected_output_single_day):
    now = datetime.datetime(2014, 3, 19, 18, 30)

    actual_output = io.StringIO()
    report_handler = ReportHandler(args, now, activities)
    report_handler.output = actual_output
    report_handler()
    assert expected_output_single_day == actual_output.getvalue()
