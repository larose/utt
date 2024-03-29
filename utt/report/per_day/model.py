import datetime
import itertools
from typing import Dict, List

from utt.data_structures.activity import Activity
from utt.report import formatter
from utt.report.common import filter_activities_by_type


class PerDayModel:
    def __init__(self, activities: List[Activity]):
        self.dates = _groupby_date(filter_activities_by_type(activities, Activity.Type.WORK))


def _groupby_date(activities: List[Activity]) -> List[Dict]:
    def key(act):
        """Key on date."""
        return act.start.date()

    result = []
    sorted_activities = sorted(activities, key=key)

    for date, activities in itertools.groupby(sorted_activities, key):
        activities = list(activities)
        duration = sum((act.duration for act in activities), datetime.timedelta())
        result.append(
            {
                "duration": formatter.format_duration(duration),
                "hours": duration,
                "date": date,
                "projects": ", ".join(
                    sorted(
                        set(act.name.project for act in activities),
                        key=lambda project: project.lower(),
                    )
                ),
                "tasks": ", ".join(
                    sorted(
                        set(act.name.task for act in activities),
                        key=lambda task: task.lower(),
                    )
                ),
            }
        )

    return sorted(result, key=lambda result: result["date"])
