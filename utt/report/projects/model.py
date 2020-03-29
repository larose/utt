import datetime
import itertools
from typing import Dict, List

from pytz.tzinfo import DstTzInfo

from ...data_structures.activity import Activity
from .. import formatter
from ..common import clip_activities_by_range, filter_activities_by_type


class ProjectsModel:
    def __init__(
        self, activities: List[Activity], start_date: datetime.date, end_date: datetime.date, local_timezone: DstTzInfo,
    ):
        activities = clip_activities_by_range(start_date, end_date, activities, local_timezone)

        self.projects = groupby_project(filter_activities_by_type(activities, Activity.Type.WORK))


def groupby_project(activities: List[Activity]) -> List[Dict]:
    def key(act):
        return act.name.project

    result = []
    sorted_activities = sorted(activities, key=key)

    for project, activities in itertools.groupby(sorted_activities, key):
        activities = list(activities)
        result.append(
            {
                "duration": formatter.format_duration(sum((act.duration for act in activities), datetime.timedelta())),
                "project": project,
                "name": ", ".join(sorted(set(act.name.task for act in activities), key=lambda task: task.lower(),)),
            }
        )

    return sorted(result, key=lambda result: result["project"].lower())
