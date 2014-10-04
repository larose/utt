from __future__ import print_function
import datetime
import itertools

from .activity import Activity


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# PUBLIC
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def print_report(report_date, activities):
    _print_date_section(report_date, activities)
    _print_projects_section(report_date, activities)
    _print_activities_section(report_date, activities)
    _print_details_section(report_date, activities)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# PRIVATE
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def _duration(activities):
    return sum((act.duration for act in activities), datetime.timedelta())

def _format_date(datetime):
    return datetime.strftime(
        "%A, %b %d, %Y (week {week})".format(week=datetime.isocalendar()[1])
    )

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
            'duration': _format_duration(
                sum((act.duration for act in activities),
                    datetime.timedelta())),
            'project': project,
            'name': ", ".join(sorted(set(act.name.task for act in activities)))
        })

    return sorted(result, key=lambda act: (act['project'].lower(),
                                           act['name'].lower()))

def _groupby_project(activities):
    def key(act):
        return act.name.project

    result = []
    sorted_activities = sorted(activities, key=key)
    for project, activities in itertools.groupby(sorted_activities, key):
        activities = list(activities)
        result.append({
            'duration': _format_duration(
                sum((act.duration for act in activities),
                    datetime.timedelta())),
            'project': project,
            'name': ", ".join(sorted(set(act.name.task for act in activities),
                                     key=lambda task: task.lower()))
        })

    return sorted(result, key=lambda result: result['project'].lower())

def _print_activities_section(report_date, activities):
    print()
    print(_title('Activities'))
    print()

    names_work = _groupby_name(list(filter(
        lambda act: act.type == Activity.Type.WORK, activities[report_date])))

    _print_dicts(names_work)

    print()

    names_break = _groupby_name(list(filter(
        lambda act: act.type == Activity.Type.BREAK, activities[report_date])))
    _print_dicts(names_break)

def _print_date_section(report_date, activities):
    print()
    print(_title(_format_date(report_date)))
    print()

    _print_time("Working Time", report_date, activities, Activity.Type.WORK)
    _print_time("Break   Time", report_date, activities, Activity.Type.BREAK)

def _print_details_section(report_date, activities):
    print()
    print(_title('Details'))
    print()

    for activity in activities[report_date]:
        print("(%s) %s-%s %s" % (_format_duration(activity.duration),
                                 _format_time(activity.start),
                                 _format_time(activity.end),
                                 activity.name))

    print()

def _print_dicts(dcts):
    format_string = "({duration}) {project:<{projects_max_length}}: {name}"

    projects = (dct['project'] for dct in dcts)
    projects_max_length = max(
        itertools.chain([0], (len(project) for project in projects)))
    context = {'projects_max_length': projects_max_length}
    for dct in dcts:
        print(format_string.format(**dict(context, **dct)))

def _print_projects_section(report_date, activities):
    print()
    print(_title('Projects'))
    print()

    projects = _groupby_project(list(filter(
        lambda act: act.type == Activity.Type.WORK, activities[report_date])))

    _print_dicts(projects)

def _print_time(name, report_date, activities, activity_type):
    report_date_duration = _duration(filter(
        lambda act: act.type == activity_type, activities[report_date]))

    print("%s: %s" % (name, _format_duration(report_date_duration)), end='')

    if activities[report_date]:
        last_activity = activities[report_date][-1]
        if last_activity.is_current_activity and \
           last_activity.type == activity_type:
            cur_duration = last_activity.duration
            print(" (%s + %s)" % (
                _format_duration(report_date_duration - cur_duration),
                _format_duration(cur_duration)), end='')

    print(" [%s]" % _format_duration_hours_only(_total_time(activities,
                                                            activity_type)))

def _title(text):
    return '{:-^80}'.format(' ' + text + ' ')

def _total_time(activities_grouped_by_day, activity_type):
    total_time = datetime.timedelta()
    for activities_ in activities_grouped_by_day.values():
        for activity in activities_:
            if activity.type == activity_type:
                total_time += activity.duration
    return total_time
