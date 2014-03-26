import collections
import datetime
import itertools

from .activity import Activity
from .entry import Entry
from .print_report import print_report
from . import util

NAME = 'report'


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# PUBLIC
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def add_args(parser):
    parser.add_argument("report_date",
                        metavar="date",
                        default=datetime.date.today(),
                        type=_parse_date,
                        nargs='?')

    parser.add_argument("--current-activity",
                        default='-- Current Activity --',
                        type=str,
                        help="Set the current activity")

    parser.add_argument("--no-current-activity",
                        action='store_true',
                        default=False,
                        help="Do not display the current activity")

def execute(args):
    entries = _filter_and_group_entries(
        args.report_date,
        util.entries_from_file(args.data_filename))
    _add_current_entry(
        args.report_date,
        entries[args.report_date],
        args.now,
        args.current_activity,
        args.no_current_activity
    )
    activities = _activities_from_entries(entries)
    print_report(args.report_date, activities)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# PRIVATE
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def _activities_from_entries(entries_grouped_by_day):
    activities_grouped_by_day = collections.defaultdict(list)

    for date, entries in entries_grouped_by_day.items():
        activities_grouped_by_day[date] = list(
            _activities_from_entries_day(entries))

    return activities_grouped_by_day

def _activities_from_entries_day(entries):
    return (Activity(entry_pair[0].datetime, entry_pair[1])
            for entry_pair in _pairwise(entries))

def _add_current_entry(report_date, entries, now, current_activity_name,
                       disable_current_activity):
    today = now.date()
    if report_date == today and entries and entries[-1].datetime < now and \
            not disable_current_activity:
        entries.append(Entry(now, current_activity_name, True))

def _filter_and_group_entries(report_date, all_entries):
    week_start_date, week_end_date = _week_dates(report_date)

    entries = list(filter(
        _make_range_filter_fn(week_start_date, week_end_date), all_entries))

    entries_grouped_by_day = collections.defaultdict(list)

    for day, entries in itertools.groupby(
            entries, key=lambda entry: entry.datetime.date()):
        entries_grouped_by_day[day] = list(entries)

    return entries_grouped_by_day

def _make_range_filter_fn(start_date, end_date):
    def filter_fn(entry):
        date = entry.datetime.date()
        return date >= start_date and date <= end_date
    return filter_fn

def _pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

def _parse_date(datestring):
    return datetime.datetime.strptime(datestring, "%Y-%m-%d").date()

def _week_dates(date):
    week_start_date = date + datetime.timedelta(-date.weekday())
    week_end_date = date + datetime.timedelta(6 - date.weekday())
    return week_start_date, week_end_date
