import collections
import datetime
import itertools
import re

from ..  import io
from .  import template

NAME = 'report'

def add_args(parser):
    parser.add_argument("date",
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
    context = type('Context', (object,), {})
    context.args = args

    entries = list(filter(_make_day_filter(args.date),
                          io.entries(args.data_filename)))

    context.current_activity = None
    current_entry = _current_entry(
        args.date,
        entries, datetime.date.today(),
        datetime.datetime.now(),
        args.current_activity,
        args.no_current_activity)

    if current_entry:
        entries.append(current_entry)

    context.activities = list(_entries2activities(entries))

    context.work = _make_sub_context(context, 'Work', _ActivityType.WORK)
    context.break_ = _make_sub_context(context, 'Break', _ActivityType.BREAK)

    context.work.current_activity = None
    context.break_.current_activity = None
    if current_entry:
        if context.activities[-1].type == _ActivityType.WORK:
            context.work.current_activity = context.activities[-1]
        elif context.activities[-1].type == _ActivityType.BREAK:
            context.break_.current_activity = context.activities[-1]

    template.plain_text_format(context)

_project_regex = re.compile("(?P<project>[^\s:]+):\s(?P<name>.*)")

class _Activity:
    def __init__(self, name, start, end, type):
        self.name = name
        self.start = start
        self.end = end
        self.duration = end - start
        self.type = type

class _ActivityType:
    WORK = 0
    BREAK = 1
    IGNORED = 2

class _Name:
    def __init__(self, name, task, project):
        self.name = name
        self.task = task
        self.project = project

    def __lt__(self, other):
        return self.name < other.name

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name

class _Project:

    def __init__(self, name, activities):
        self._name = name
        self._activities = activities
        self._duration = sum(map(lambda act: act.duration, self._activities),
                             datetime.timedelta())

    name = property(lambda self: self._name)
    activities = property(lambda self: self._activities)
    duration = property(lambda self: self._duration)

_GroupedActivity = collections.namedtuple('GroupedActivity',
                                         ['project', 'name', 'duration'])

def _current_entry(date, entries, today, now, name, no_current):
    if date == today and entries and entries[-1].datetime < now and \
            not no_current:
        return io.Entry(now, name)

def _duration(activities):
    return sum(map(lambda act: act.duration, activities), datetime.timedelta())

def _entries2activities(entries):
    a, b = itertools.tee(entries, 2)

    try:
        first_entry = next(a)
    except StopIteration:
        return []

    it = map(lambda entries: _entries2activity(*entries),
             _pairwise(itertools.chain([first_entry], b)))

    # We ignore the first item because it is "hello".
    next(it)
    return it

def _entries2activity(entry1, entry2):

    def name2type(name):
        if name[-3:] == '***':
            return _ActivityType.IGNORED
        if name[-2:] == '**':
            return _ActivityType.BREAK
        return _ActivityType.WORK

    def name2task_project(name):
        match = _project_regex.match(name)
        if match is None:
            return name, ''
        groupdict = match.groupdict()
        return groupdict['name'], groupdict['project']

    task, project = name2task_project(entry2.activity)
    return _Activity(_Name(entry2.activity, task, project),
                    entry1.datetime, entry2.datetime, 
                    name2type(entry2.activity))

def _groupby(iterable, group_key, aggregate, sort_key):
    def _force_list(key, value):
        return key, list(value)

    data = sorted(iterable, key=group_key)
    return sorted(map(lambda args: aggregate(*args),
                      map(lambda args: _force_list(*args),
                          itertools.groupby(data, group_key))),
                  key=sort_key)

def _groupby_name(iterable):
    def _name_aggregate(name, activities):
        return _GroupedActivity(name.project,
                                name.task,
                                _duration(activities))

    return _groupby(iterable, lambda act: act.name, _name_aggregate,
                    lambda n: (n.project, n.name))

def _groupby_project(iterable):
    def _project_aggregate(name, activities):
        return _Project(name, activities)

    return _groupby(iterable, lambda act: act.name.project, _project_aggregate,
                    lambda p: p.name)
    
def _make_day_filter(date):
    def day_filter(entry):
        return date == entry.datetime.date()
    return day_filter

def _make_sub_context(context, name, activity_type):
    sub_context = type(name, (object,), {})
    sub_context.activities = list(
        filter(lambda act: act.type == activity_type,
               context.activities))
    sub_context.duration = _duration(sub_context.activities)
    sub_context.projects = _groupby_project(sub_context.activities)
    sub_context.names = _groupby_name(sub_context.activities)
    return sub_context

def _pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

def _parse_date(datestring):
    return datetime.datetime.strptime(datestring, "%Y-%m-%d").date()
