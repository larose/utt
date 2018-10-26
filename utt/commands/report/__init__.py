import datetime
import sys

from ...activity import Activity
from .print_report import print_report
from .common import clip_activities_by_range, filter_activities_by_type
from .summary_section import SummaryModel


class ReportHandler:
    def __init__(self, args, now, activities):
        self._args = args
        self._now = now
        self._activities = activities
        self.output = sys.stdout

    def __call__(self):
        today = self._now.date()
        if self._args.report_date is None:
            report_date = today
        else:
            report_date = _parse_date(self._now, self._args.report_date)

        report_start_date = (report_date if self._args.from_date is None else
                             self._args.from_date)
        report_end_date = (report_date if self._args.to_date is None else
                           self._args.to_date)

        if report_start_date == report_end_date:
            collect_from_date, collect_to_date = _week_dates(report_start_date)
        else:
            collect_from_date = report_start_date
            collect_to_date = report_end_date

        collect_to_date = min(today, collect_to_date)
        collect_from_date = min(today, collect_from_date)

        activities = self._activities()
        _add_current_activity(
            activities, self._now, self._args.current_activity,
            self._args.no_current_activity, report_start_date, report_end_date)

        activities = list(
            _filter_activities_by_range(activities, collect_from_date,
                                        collect_to_date))

        report = Report(activities, report_start_date, report_end_date)

        print_report(report, report_start_date, report_end_date, activities,
                     self.output)


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


def _filter_activities_by_range(activities, start_date, end_date):
    start_datetime = datetime.datetime(start_date.year, start_date.month,
                                       start_date.day)
    end_datetime = datetime.datetime(end_date.year, end_date.month,
                                     end_date.day, 23, 59, 59, 99999)

    for full_activity in activities:
        activity = full_activity.clip(start_datetime, end_datetime)
        if activity.duration > datetime.timedelta():
            yield activity


# pylint: disable=too-many-arguments
def _add_current_activity(activities, now, current_activity_name,
                          disable_current_activity, report_start_date,
                          report_end_date):

    if not activities or disable_current_activity:
        return

    today = now.date()
    report_is_today = today == report_start_date and today == report_end_date
    now_is_after_last_activity = activities[-1].end < now

    if report_is_today and now_is_after_last_activity:
        activities.append(
            Activity(current_activity_name, activities[-1].end, now, True))


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


class Report:
    def __init__(self, activities, start_date, end_date):
        self.summary_model = SummaryModel(activities, start_date, end_date)
