from __future__ import print_function

import datetime
import itertools

from . import formatter
from ..activity import Activity
from .common import (clip_activities_by_range, filter_activities_by_type,
                     print_dicts)


class ProjectsModel:
    def __init__(self, activities, start_date, end_date, local_timezone):
        activities = clip_activities_by_range(start_date, end_date, activities,
                                              local_timezone)

        self.projects = _groupby_project(
            filter_activities_by_type(activities, Activity.Type.WORK))


class ProjectsView:
    def __init__(self, model):
        self._model = model

    def render(self, output):
        print(file=output)
        print(formatter.title('Projects'), file=output)
        print(file=output)

        print_dicts(self._model.projects, output)


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
