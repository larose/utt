import itertools
from datetime import timedelta
from typing import Dict, List, Optional

from ...data_structures.activity import Activity
from .. import formatter
from ..common import filter_activities_by_type


class ProjectSummaryModel:
    def __init__(self, activities: List[Activity]):
        work_activities = filter_activities_by_type(activities, Activity.Type.WORK)
        self.projects = _groupby_project_sorted_by_duration(work_activities)
        self.current_activity = _get_current_activity_info(activities)
        self.total_duration = self._calculate_total_duration()

    def _calculate_total_duration(self) -> str:
        total = sum((project["duration_obj"] for project in self.projects), timedelta())
        if self.current_activity:
            total += self.current_activity["duration_obj"]
        return formatter.format_duration(total)


def _get_current_activity_info(activities: List[Activity]) -> Optional[Dict]:
    for activity in activities:
        if activity.is_current_activity:
            return {
                "name": activity.name.name,
                "duration": formatter.format_duration(activity.duration),
                "duration_obj": activity.duration,
            }
    return None


def _groupby_project_sorted_by_duration(activities: List[Activity]) -> List[Dict]:
    def key(act):
        return act.name.project

    non_current_activities = [act for act in activities if not act.is_current_activity]
    result = []
    sorted_activities = sorted(non_current_activities, key=key)

    for project, activities in itertools.groupby(sorted_activities, key):
        activities = list(activities)
        total_duration = sum((act.duration for act in activities), timedelta())
        result.append(
            {
                "duration": formatter.format_duration(total_duration),
                "project": project,
                "duration_obj": total_duration,
            }
        )

    return sorted(result, key=lambda result: result["duration_obj"], reverse=True)
