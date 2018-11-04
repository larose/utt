from __future__ import print_function

import datetime
import itertools

from . import formatter
from ..activity import Activity
from .common import (clip_activities_by_range, filter_activities_by_type,
                     print_dicts)


class ActivitiesModel:
    def __init__(self, activities, start_date, end_date, local_timezone):
        activities = clip_activities_by_range(start_date, end_date, activities,
                                              local_timezone)
        self.names_work = _groupby_name(
            filter_activities_by_type(activities, Activity.Type.WORK))
        self.names_break = _groupby_name(
            filter_activities_by_type(activities, Activity.Type.BREAK))


class ActivitiesView:
    def __init__(self, model):
        self._model = model

    def render(self, output):
        print(file=output)
        print(formatter.title('Activities'), file=output)
        print(file=output)

        print_dicts(self._model.names_work, output)

        print(file=output)

        print_dicts(self._model.names_break, output)


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
            'project':
            project,
            'duration':
            formatter.format_duration(
                sum((act.duration for act in activities),
                    datetime.timedelta())),
            'name':
            ", ".join(sorted(set(act.name.task for act in activities)))
        })

    return sorted(
        result, key=lambda act: (act['project'].lower(), act['name'].lower()))
