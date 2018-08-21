from __future__ import print_function
import datetime
import itertools

from .activity import Activity

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# PUBLIC
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def print_report(start_date, end_date, activities):
    _print_date_section(start_date, end_date, activities)
    _print_projects_section(start_date, end_date, activities)
    _print_activities_section(start_date, end_date, activities)
    if start_date == end_date:
        _print_details_section(start_date, activities)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# PRIVATE
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def _duration(activities):
    return sum((act.duration for act in activities), datetime.timedelta())


def _format_date(datetime):
    return datetime.strftime(
        "%A, %b %d, %Y (week {week})".format(week=datetime.isocalendar()[1]))


def _format_duration(duration):
    mm, ss = divmod(duration.seconds, 60)
    hh, mm = divmod(mm, 60)
    s = "%dh%02d" % (hh, mm)
    if duration.days:

        def plural(n):
            return n, abs(n) != 1 and "s" or ""

        s = ("%d day%s, " % plural(duration.days)) + s
    return s


def _format_duration_hours_only(duration):
    mm, ss = divmod(duration.seconds, 60)
    hh, mm = divmod(mm, 60)
    hh += duration.days * 24
    s = "%dh%02d" % (hh, mm)
    return s


def _format_time(datetime):
    return datetime.strftime("%H:%M")


def _groupby_name(activities):
    def key(act):
        return act.name.name

    result = []
    sorted_activities = sorted(activities, key=key)
    for name, activities in itertools.groupby(sorted_activities, key):
        activities = list(activities)
        project = activities[0].name.project
        result.append({
            'duration':
            _format_duration(
                sum((act.duration
                     for act in activities), datetime.timedelta())),
            'project':
            project,
            'name':
            ", ".join(sorted(set(act.name.task for act in activities)))
        })

    return sorted(
        result, key=lambda act: (act['project'].lower(), act['name'].lower()))


def _groupby_project(activities):
    def key(act):
        return act.name.project

    result = []
    sorted_activities = sorted(activities, key=key)
    for project, activities in itertools.groupby(sorted_activities, key):
        activities = list(activities)
        result.append({
            'duration':
            _format_duration(
                sum((act.duration
                     for act in activities), datetime.timedelta())),
            'project':
            project,
            'name':
            ", ".join(
                sorted(
                    set(act.name.task for act in activities),
                    key=lambda task: task.lower()))
        })

    return sorted(result, key=lambda result: result['project'].lower())


def _print_activities_section(start_date, end_date, activities):
    print()
    print(_title('Activities'))
    print()

    activities = _clip_activities_by_range(start_date, end_date, activities)
    names_work = _groupby_name(
        _filter_activities_by_type(activities, Activity.Type.WORK))
    _print_dicts(names_work)

    print()

    names_break = _groupby_name(
        _filter_activities_by_type(activities, Activity.Type.BREAK))
    _print_dicts(names_break)


def _print_date_section(start_date, end_date, activities):
    print()
    date_str = _format_date(start_date)
    if end_date != start_date:
        date_str = " ".join([date_str, "to", _format_date(end_date)])
    print(_title(date_str))

    print()
    _print_time("Working Time", start_date, end_date, activities,
                Activity.Type.WORK)
    _print_time("Break   Time", start_date, end_date, activities,
                Activity.Type.BREAK)


def _print_details_section(report_date, activities):
    print()
    print(_title('Details'))
    print()

    activities = _clip_activities_by_range(report_date, report_date,
                                           activities)
    for activity in activities:
        print("(%s) %s-%s %s" % (_format_duration(activity.duration),
                                 _format_time(activity.start),
                                 _format_time(activity.end), activity.name))

    print()


def _print_dicts(dcts):
    format_string = "({duration}) {project:<{projects_max_length}}: {name}"

    projects = (dct['project'] for dct in dcts)
    projects_max_length = max(
        itertools.chain([0], (len(project) for project in projects)))
    context = {'projects_max_length': projects_max_length}
    for dct in dcts:
        print(format_string.format(**dict(context, **dct)))


def _print_ignored_overnights(start_date, end_date, activities):
    activities = _clip_activities_by_range(start_date, end_date, activities)
    if activities:
        print("WARN: Ignored {} overnight {}, total time: {}".format(
            len(activities), "activities" if len(activities) > 1 else
            "activity", _format_duration(_duration(activities))))


def _print_projects_section(start_date, end_date, activities):
    print()
    print(_title('Projects'))
    print()

    activities = _clip_activities_by_range(start_date, end_date, activities)

    projects = _groupby_project(
        _filter_activities_by_type(activities, Activity.Type.WORK))
    _print_dicts(projects)


def _print_time(name, start_date, end_date, activities, activity_type):
    activities = _filter_activities_by_type(activities, activity_type)
    ranged_activities = _clip_activities_by_range(start_date, end_date,
                                                  activities)

    report_date_duration = _duration(ranged_activities)

    print("%s: %s" % (name, _format_duration(report_date_duration)), end='')

    if ranged_activities:
        last_activity = ranged_activities[-1]
        if last_activity.is_current_activity and \
           last_activity.type == activity_type:
            cur_duration = last_activity.duration
            print(
                " (%s + %s)" %
                (_format_duration(report_date_duration - cur_duration),
                 _format_duration(cur_duration)),
                end='')
    if start_date == end_date:
        print(" [%s]" % _format_duration_hours_only(_duration(activities)))
    else:
        print()


def _title(text):
    return '{:-^80}'.format(' ' + text + ' ')


def _total_time(activities_grouped_by_day, activity_type):
    total_time = datetime.timedelta()
    for activities_ in activities_grouped_by_day.values():
        for activity in activities_:
            if activity.type == activity_type:
                total_time += activity.duration
    return total_time


def _clip_activities_by_range(start_date, end_date, activities):
    """ Clip a list of Activity with the given range, remove activities
    which have zero durations

    Parameters
    ----------
    start_date : datetime.date
    end_date : datetime.date
    activities : list of Activity

    Returns
    -------
    clipped: list of Activity
    """
    delta = datetime.timedelta()
    start_dt = datetime.datetime(start_date.year, start_date.month,
                                 start_date.day)
    end_dt = datetime.datetime(end_date.year, end_date.month, end_date.day, 23,
                               59, 59, 99999)
    new_activities = []
    for activity in activities:
        clipped = activity.clip(start_dt, end_dt)
        if clipped.duration > delta:
            new_activities.append(clipped)
    return new_activities


def _filter_activities_by_type(activities, activity_type):
    """ Filter a list of Activity with the given activity type.

    Parameters
    ----------
    activities : list of Activity
    activity_type : str
        An activity type defined in Activity.Type

    Returns
    -------
    filtered: list of Activity
    """
    return list(filter(lambda act: act.type == activity_type, activities))
