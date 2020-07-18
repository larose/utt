import argparse
import calendar
import datetime
from enum import Enum, auto
from typing import NamedTuple, Optional

from ..fromisocalendar import date_fromisocalendar
from .now import Now


class CSVSection(Enum):
    per_day = auto()


csv_section_name_to_csv_section = {"per-day": CSVSection.per_day, "per_day": CSVSection.per_day}


class DateRange(NamedTuple):
    start: datetime.date
    end: datetime.date


class ReportArgs(NamedTuple):
    range: DateRange
    current_activity_name: Optional[str]
    project_name_filter: Optional[str]
    csv_section: Optional[CSVSection]
    show_comments: bool
    show_details: bool
    show_per_day: bool


def parse_report_range_arguments(
    unparsed_report_date: Optional[str],
    unparsed_month: Optional[str],
    unparsed_week: Optional[str],
    unparsed_from_date: Optional[str],
    unparsed_to_date: Optional[str],
    today: datetime.date,
) -> DateRange:
    if unparsed_report_date is None:
        report_date = today
    else:
        report_date = parse_date(today, unparsed_report_date)

    if unparsed_month:
        report_start_date, report_end_date = parse_month(report_date, unparsed_month)
    elif unparsed_week:
        report_start_date, report_end_date = parse_week(report_date, unparsed_week)
    else:
        report_start_date = report_end_date = report_date

    report_start_date = (
        report_start_date if unparsed_from_date is None else parse_date(today, unparsed_from_date, is_past=True)
    )
    report_end_date = (
        report_end_date if unparsed_to_date is None else parse_date(report_start_date, unparsed_to_date, is_past=False)
    )

    return DateRange(start=report_start_date, end=report_end_date)


def parse_date(today, datestring, is_past=True):
    day = parse_relative_day(today, datestring)
    if day is not None:
        return day
    date = parse_relative_date(today, datestring, is_past=is_past)
    if date is not None:
        return date
    return parse_absolute_date(datestring)


def parse_absolute_date(datestring):
    return datetime.datetime.strptime(datestring, "%Y-%m-%d").date()


def parse_relative_day(today, datestring):
    """Parses day like 'today' or 'yesterday'.

    Note that 'today' has the same effect as "not supplying a date" but
    it's included for completeness.
    """
    if "TODAY".startswith(datestring.upper()):
        return today
    if "YESTERDAY".startswith(datestring.upper()):
        return today - datetime.timedelta(days=1)
    return None


def parse_day(day):
    day_upper = day.upper()
    if day_upper in DAY_NAMES:
        return day_upper
    return None


def parse_relative_date(today, datestring, is_past):
    day = parse_day(datestring)
    if day is None:
        return None
    now_weekday_offset = today.weekday()
    report_weekday_offset = DAY_NAMES.index(day)
    if is_past:
        delta = now_weekday_offset - report_weekday_offset
        delta = -(delta % 7)
    else:
        delta = report_weekday_offset - now_weekday_offset
        delta = delta % 7
    return today + datetime.timedelta(days=delta)


def parse_relative_month(today, monthstring):
    month = parse_integer_month(today, monthstring)
    if month is not None:
        return month
    if len(monthstring) < 3:
        # ambiguous month
        return None
    month_upper = monthstring.upper()
    for i, monthname in enumerate(MONTH_NAMES):
        if monthname.startswith(month_upper):
            month = i + 1
            break
    else:
        if "THIS".startswith(month_upper):
            month = today.month
        elif "PREVIOUS".startswith(month_upper):
            month = today.month - 1
            if month == 0:
                month = 12
        else:
            return None

    year = today.year if month <= today.month else (today.year - 1)
    return datetime.date(year, month, 1)


def parse_integer_month(today, monthstring):
    """Parse integer month

    This can be a month number (10 -- Oct)
    or a negative number (-2 -- 2 months ago).
    """
    try:
        monthnum = int(monthstring)
    except ValueError:
        return None

    if monthnum == 0:
        return None
    elif monthnum < 0:
        if monthnum < -11:
            return None
        monthnum = today.month + monthnum
        if monthnum < 1:
            monthnum += 12
        if monthnum < 1:
            return None
    year = today.year
    if monthnum > today.month:
        year -= 1
    return datetime.date(year, monthnum, 1)


def parse_absolute_month(monthstring):
    return datetime.datetime.strptime(monthstring, "%Y-%m").date()


def parse_month(today, monthstring):
    month = parse_relative_month(today, monthstring)
    if month is None:
        month = parse_absolute_month(monthstring)
    (_month_weekday, month_days) = calendar.monthrange(month.year, month.month)
    start = month
    end = month.replace(day=month_days)

    return (start, end)


def parse_relative_week(today, weekstring):
    """Try to parse a week string ('this' or 'previous').

    Return the first day of the week as a datetime.date
    """
    week_upper = weekstring.upper()
    if "THIS".startswith(week_upper):
        (year, week, _d) = today.isocalendar()
    elif "PREVIOUS".startswith(week_upper):
        (year, week, _d) = (today - datetime.timedelta(days=7)).isocalendar()
    else:
        return None
    return date_fromisocalendar(year, week, 1)


def parse_week_number(today, weekstring):
    try:
        weeknum = int(weekstring)
    except ValueError:
        return None

    if weeknum == 0:
        return None
    elif weeknum < 0:
        one_week = datetime.timedelta(days=7)
        # Note: weeknum is negative so this effectively subtracts
        (year, week, _d) = (today + weeknum * one_week).isocalendar()
        return date_fromisocalendar(year, week, 1)
    else:
        (year, week, _d) = today.isocalendar()
        if weeknum > week:
            year -= 1
        return date_fromisocalendar(year, weeknum, 1)


def parse_week(today, weekstring):
    week = parse_relative_week(today, weekstring)
    if week is None:
        week = parse_week_number(today, weekstring)
    start = week
    end = week + datetime.timedelta(days=6)

    return (start, end)


def week_dates(date):
    week_start_date = date + datetime.timedelta(-date.weekday())
    week_end_date = date + datetime.timedelta(6 - date.weekday())
    return week_start_date, week_end_date


DAY_NAMES = [
    "MONDAY",
    "TUESDAY",
    "WEDNESDAY",
    "THURSDAY",
    "FRIDAY",
    "SATURDAY",
    "SUNDAY",
]
MONTH_NAMES = [
    "JANUARY",
    "FEBRUARY",
    "MARCH",
    "APRIL",
    "MAY",
    "JUNE",
    "JULY",
    "AUGUST",
    "SEPTEMBER",
    "OCTOBER",
    "NOVEMBER",
    "DECEMBER",
]


def report_args(args: argparse.Namespace, now: Now) -> ReportArgs:
    report_range = parse_report_range_arguments(
        unparsed_report_date=args.report_date,
        unparsed_month=args.month,
        unparsed_week=args.week,
        unparsed_from_date=args.from_date,
        unparsed_to_date=args.to_date,
        today=now.date(),
    )

    current_activity_name = args.current_activity
    if args.no_current_activity:
        current_activity_name = None

    return ReportArgs(
        range=report_range,
        current_activity_name=current_activity_name,
        project_name_filter=args.project,
        csv_section=csv_section_name_to_csv_section.get(args.csv_section),
        show_comments=args.comments,
        show_details=args.details,
        show_per_day=args.per_day,
    )
