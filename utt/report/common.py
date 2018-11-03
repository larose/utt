from __future__ import print_function

import datetime
import itertools


def print_dicts(dcts, output):
    format_string = "({duration}) {project:<{projects_max_length}}: {name}"

    projects = (dct['project'] for dct in dcts)
    projects_max_length = max(
        itertools.chain([0], (len(project) for project in projects)))
    context = {'projects_max_length': projects_max_length}
    for dct in dcts:
        print(format_string.format(**dict(context, **dct)), file=output)


def clip_activities_by_range(start_date, end_date, activities, local_timezone):
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
    start_dt = local_timezone.localize(
        datetime.datetime(start_date.year, start_date.month, start_date.day))
    end_dt = local_timezone.localize(
        datetime.datetime(end_date.year, end_date.month, end_date.day, 23, 59,
                          59, 99999))
    new_activities = []
    for activity in activities:
        clipped = activity.clip(start_dt, end_dt)
        if clipped.duration > delta:
            new_activities.append(clipped)
    return new_activities


def filter_activities_by_type(activities, activity_type):
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
