from __future__ import print_function
import datetime
import itertools

from ...activity import Activity
from .common import clip_activities_by_range, filter_activities_by_type
from .summary_section import SummaryView
from . import formatter

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# PUBLIC
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def print_report(report, output):
    start_date = report.start_date
    end_date = report.end_date
    activities = report.activities

    SummaryView(report.summary_model).render(output)
    _print_projects_section(start_date, end_date, activities, output)
    _print_activities_section(start_date, end_date, activities, output)
    if start_date == end_date:
        _print_details_section(start_date, activities, output)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# PRIVATE
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# pylint: disable=redefined-outer-name
def _format_time(datetime):
    return datetime.strftime("%H:%M")


def _groupby_name(activities):
    def key(act):
        return act.name.name

    result = []
    sorted_activities = sorted(activities, key=key)
    # pylint: disable=redefined-argument-from-local
    for _, activities in itertools.groupby(sorted_activities, key):
        activities = list(activities)
        project = activities[0].name.project
        result.append({
            'duration':
            formatter.format_duration(
                sum((act.duration for act in activities),
                    datetime.timedelta())),
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
    # pylint: disable=redefined-argument-from-local
    for project, activities in itertools.groupby(sorted_activities, key):
        activities = list(activities)
        result.append({
            'duration':
            formatter.format_duration(
                sum((act.duration for act in activities),
                    datetime.timedelta())),
            'project':
            project,
            'name':
            ", ".join(
                sorted(
                    set(act.name.task for act in activities),
                    key=lambda task: task.lower()))
        })

    return sorted(result, key=lambda result: result['project'].lower())


def _print_activities_section(start_date, end_date, activities, output):
    print(file=output)
    print(formatter.title('Activities'), file=output)
    print(file=output)

    activities = clip_activities_by_range(start_date, end_date, activities)
    names_work = _groupby_name(
        filter_activities_by_type(activities, Activity.Type.WORK))
    _print_dicts(names_work, output)

    print(file=output)

    names_break = _groupby_name(
        filter_activities_by_type(activities, Activity.Type.BREAK))
    _print_dicts(names_break, output)


def _print_details_section(report_date, activities, output):
    print(file=output)
    print(formatter.title('Details'), file=output)
    print(file=output)

    activities = clip_activities_by_range(report_date, report_date, activities)
    for activity in activities:
        print(
            "(%s) %s-%s %s" % (formatter.format_duration(activity.duration),
                               _format_time(activity.start),
                               _format_time(activity.end), activity.name),
            file=output)

    print(file=output)


def _print_dicts(dcts, output):
    format_string = "({duration}) {project:<{projects_max_length}}: {name}"

    projects = (dct['project'] for dct in dcts)
    projects_max_length = max(
        itertools.chain([0], (len(project) for project in projects)))
    context = {'projects_max_length': projects_max_length}
    for dct in dcts:
        print(format_string.format(**dict(context, **dct)), file=output)


def _print_projects_section(start_date, end_date, activities, output):
    print(file=output)
    print(formatter.title('Projects'), file=output)
    print(file=output)

    activities = clip_activities_by_range(start_date, end_date, activities)

    projects = _groupby_project(
        filter_activities_by_type(activities, Activity.Type.WORK))
    _print_dicts(projects, output)
