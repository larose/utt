import datetime
import itertools
import sys

from .activity import Activity
from .. import hello
from ...entry import Entry
from .print_report import print_report


class ReportHandler:
    def __init__(self, args, log_repo, now):
        self._args = args
        self._now = now
        self._log_repo = log_repo
        self._output = sys.stdout

    def __call__(self):
        args = self._args

        today = self._now.date()
        if args.report_date is None:
            report_date = today
        else:
            report_date = _parse_date(self._now, args.report_date)

        report_start_date = (report_date
                             if args.from_date is None else args.from_date)
        report_end_date = (report_date
                           if args.to_date is None else args.to_date)

        if report_start_date == report_end_date:
            collect_from_date, collect_to_date = _week_dates(report_start_date)
        else:
            collect_from_date = report_start_date
            collect_to_date = report_end_date

        collect_to_date = min(today, collect_to_date)
        collect_from_date = min(today, collect_from_date)
        entries = list(self._log_repo.entries())
        _add_current_entry(entries, self._now, args.current_activity,
                           args.no_current_activity, report_start_date,
                           report_end_date)
        activities = _collect_activities(collect_from_date, collect_to_date,
                                         entries)
        print_report(report_start_date, report_end_date, activities,
                     self._output)


class ReportCommand:
    NAME = 'report'
    DESCRIPTION = 'Summarize tasks for given time period'

    Handler = ReportHandler

    @staticmethod
    def add_args(parser):
        parser.add_argument("report_date", metavar="date", type=str, nargs='?')

        parser.add_argument(
            "--current-activity",
            default='-- Current Activity --',
            type=str,
            help="Set the current activity")

        parser.add_argument(
            "--no-current-activity",
            action='store_true',
            default=False,
            help="Do not display the current activity")

        parser.add_argument(
            "--from",
            default=None,
            dest="from_date",
            type=_parse_absolute_date,
            help="Specify an inclusive start date to report.")

        parser.add_argument(
            "--to",
            default=None,
            dest="to_date",
            type=_parse_absolute_date,
            help="Specify an inclusive end date to report.")


Command = ReportCommand

DAY_NAMES = [
    "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY",
    "SUNDAY"
]


def _collect_activities(start_date, end_date, entries):
    start_datetime = datetime.datetime(start_date.year, start_date.month,
                                       start_date.day)
    end_datetime = datetime.datetime(end_date.year, end_date.month,
                                     end_date.day, 23, 59, 59, 99999)
    start_datetime = start_datetime
    end_datetime = end_datetime
    activities = []
    for prev_entry, next_entry in _pairwise(entries):
        if next_entry.name == hello.HelloCommand.NAME:
            continue

        full_activity = Activity(prev_entry.datetime, next_entry)
        activity = full_activity.clip(start_datetime, end_datetime)
        if activity.duration > datetime.timedelta():
            activities.append(activity)

    return sorted(activities, key=lambda act: act.start)


# pylint: disable=too-many-arguments
def _add_current_entry(entries, now, current_activity_name,
                       disable_current_activity, report_start_date,
                       report_end_date):
    today = now.date()
    if (today >= report_start_date and today <= report_end_date and entries
            and entries[-1].datetime < now and not disable_current_activity):
        entries.append(Entry(now, current_activity_name, True))


# pylint: disable=invalid-name
def _pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def _parse_absolute_date(datestring):
    return datetime.datetime.strptime(datestring, "%Y-%m-%d").date()


def _parse_date(now, datestring):
    date = _parse_relative_date(now, datestring)
    if date is not None:
        return date
    return _parse_absolute_date(datestring)


def _parse_day(day):
    day_upper = day.upper()
    if day_upper in DAY_NAMES:
        return day_upper
    return None


def _parse_relative_date(now, datestring):
    day = _parse_day(datestring)
    if day is None:
        return None
    now_weekday_offset = now.weekday()
    report_weekday_offset = DAY_NAMES.index(day)
    delta = now_weekday_offset - report_weekday_offset
    if delta < 0:
        delta += len(DAY_NAMES)
    return now.date() - datetime.timedelta(days=delta)


def _week_dates(date):
    week_start_date = date + datetime.timedelta(-date.weekday())
    week_end_date = date + datetime.timedelta(6 - date.weekday())
    return week_start_date, week_end_date
