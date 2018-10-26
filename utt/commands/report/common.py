import datetime


def clip_activities_by_range(start_date, end_date, activities):
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
