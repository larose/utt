import collections
import datetime
import itertools

from .activity import Activity
from .entry import Entry
from .print_report import print_report
from . import util

from .cmd_hello import HELLO

NAME = 'report'


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# PUBLIC
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def add_args(parser):
    parser.add_argument("report_date",
                        metavar="date",
                        type=str,
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
    report_date = None
    if args.report_date is None:
        report_date = args.now.date()
    else:
        report_date = _parse_date(args.now, args.report_date)

    entries = _filter_and_group_entries(
        report_date,
        util.entries_from_file(args.data_filename)
    )
    entries[report_date] = _fetch_entries_of_day(entries, report_date)
    _add_current_entry(
        report_date,
        entries[report_date],
        args.now,
        args.current_activity,
        args.no_current_activity
    )
    activities = _activities_from_entries(entries)
    print_report(report_date, activities)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# PRIVATE
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def _adjust_entry(report_date, entry, isBeginning):
    "resets datetime object to same day like report date but close to midnight"
    datetime_to_reset = entry.datetime
    datetime_to_reset = datetime_to_reset.replace(day=report_date.day)
    if isBeginning:
        datetime_to_reset = datetime_to_reset.replace(hour=0, minute=0)
        entry.name += " (started the day before)"
    else:
        datetime_to_reset = datetime_to_reset.replace(hour=23, minute=59)
        entry.name += " (finishes a day later)"
    entry.datetime = datetime_to_reset 

def _fetch_entries_of_day(entries, report_date):
    "fetches all entries of the specified date plus the ones overlapping"
    
    if not entries and not entries[report_date]:
        return []
            
    result = entries[report_date][:]
    
    day_before = report_date - datetime.timedelta(1)
    if (entries[report_date][0].name != HELLO
        and day_before in entries
        and entries[day_before]):
        last_entry = Entry.from_string(str(entries[day_before][-1]))
        _adjust_entry(report_date, last_entry, True)
        result.insert(0, last_entry)
        
    day_after = report_date + datetime.timedelta(1)
    if (day_after in entries
        and entries[day_after] 
        and entries[day_after][0].name != HELLO):
        next_entry = Entry.from_string(str(entries[day_after][0]))
        _adjust_entry(report_date, next_entry, False)
        result.append(next_entry)

    return result
    
DAY_NAMES = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]

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
