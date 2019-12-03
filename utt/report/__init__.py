import datetime
import calendar

from ..activity import Activity
from .model import Report
from ..commands.hello import HelloCommand


def report(args, now, activities, local_timezone):
    today = now.date()
    if args.report_date is None:
        report_date = today
    else:
        report_date = _parse_date(today, args.report_date)

    if args.month:
        report_start_date, report_end_date = _parse_month(
            report_date, args.month)
    elif args.week:
        report_start_date, report_end_date = _parse_week(
            report_date, args.week)
    else:
        report_start_date = report_end_date = report_date

    report_start_date = (report_start_date if args.from_date is None else
                         _parse_date(today, args.from_date, is_past=True))
    report_end_date = (report_end_date
                       if args.to_date is None else _parse_date(
                           report_start_date, args.to_date, is_past=False))

    if report_start_date == report_end_date:
        collect_from_date, collect_to_date = _week_dates(report_start_date)
    else:
        collect_from_date = report_start_date
        collect_to_date = report_end_date

    collect_to_date = min(today, collect_to_date)
    collect_from_date = min(today, collect_from_date)

    activities_ = activities()
    _add_current_activity(activities_, now, args.current_activity,
                          args.no_current_activity, report_start_date,
                          report_end_date)

    activities_ = _remove_hello_activities(activities_)

    activities_ = _filter_activities_by_range(activities_, collect_from_date,
                                              collect_to_date, local_timezone)

    activities_ = _filter_activities_by_project(activities_, args.project)

    return Report(
        list(activities_), report_start_date, report_end_date, local_timezone,
        args)


DAY_NAMES = [
    "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY",
    "SUNDAY"
]


def _filter_activities_by_range(activities, start_date, end_date,
                                local_timezone):
    start_datetime = local_timezone.localize(
        datetime.datetime(start_date.year, start_date.month, start_date.day))
    end_datetime = local_timezone.localize(
        datetime.datetime(end_date.year, end_date.month, end_date.day, 23, 59,
                          59, 99999))

    for full_activity in activities:
        activity = full_activity.clip(start_datetime, end_datetime)
        if activity.duration > datetime.timedelta():
            yield activity


def _filter_activities_by_project(activities, project):
    for activity in activities:
        if project is None or project == activity.name.project:
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


def _parse_date(today, datestring, is_past=True):
    day = _parse_relative_day(today, datestring)
    if day is not None:
        return day
    date = _parse_relative_date(today, datestring, is_past=is_past)
    if date is not None:
        return date
    return _parse_absolute_date(datestring)


def _parse_relative_day(today, datestring):
    """Parses day like 'today' or 'yesterday'.

    Note that 'today' has the same effect as "not supplying a date" but
    it's included for completeness.
    """
    if "TODAY".startswith(datestring.upper()):
        return today
    if "YESTERDAY".startswith(datestring.upper()):
        return today - datetime.timedelta(days=1)
    return None


def _parse_day(day):
    day_upper = day.upper()
    if day_upper in DAY_NAMES:
        return day_upper
    return None


def _parse_relative_date(today, datestring, is_past):
    day = _parse_day(datestring)
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


def _parse_relative_month(today, monthstring):
    month = _parse_integer_month(today, monthstring)
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


def _parse_integer_month(today, monthstring):
    """Parse integer month

    This can be a month number (10 -- Oct)
    or a negative number (-2 -- 2 months ago).
    """
    try:
        monthnum = int(monthstring)
    except ValueError:
        return None
    # pylint: disable=no-else-return
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


def _parse_absolute_month(monthstring):
    return datetime.datetime.strptime(monthstring, "%Y-%m").date()


def _parse_month(today, monthstring):
    month = _parse_relative_month(today, monthstring)
    if month is None:
        month = _parse_absolute_month(monthstring)
    (_month_weekday, month_days) = calendar.monthrange(month.year, month.month)
    start = month
    end = month.replace(day=month_days)

    return (start, end)


def _parse_relative_week(today, weekstring):
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
    return datetime.date.fromisocalendar(year, week, 1)


def _parse_week_number(today, weekstring):
    try:
        weeknum = int(weekstring)
    except ValueError:
        return None
    # pylint: disable=no-else-return
    if weeknum == 0:
        return None
    elif weeknum < 0:
        one_week = datetime.timedelta(days=7)
        # Note: weeknum is negative so this effectively subtracts
        (year, week, _d) = (today + weeknum * one_week).isocalendar()
        return datetime.date.fromisocalendar(year, week, 1)
    else:
        (year, week, _d) = today.isocalendar()
        if weeknum > week:
            year -= 1
        return datetime.date.fromisocalendar(year, weeknum, 1)


def _parse_week(today, weekstring):
    week = _parse_relative_week(today, weekstring)
    if week is None:
        week = _parse_week_number(today, weekstring)
    start = week
    end = week + datetime.timedelta(days=6)

    return (start, end)


def _remove_hello_activities(activities_):
    for activity in activities_:
        if activity.name.name != HelloCommand.NAME:
            yield activity


def _week_dates(date):
    week_start_date = date + datetime.timedelta(-date.weekday())
    week_end_date = date + datetime.timedelta(6 - date.weekday())
    return week_start_date, week_end_date
