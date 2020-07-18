import datetime
from typing import List

from ...components.report_args import DateRange
from ...data_structures.activity import Activity
from ..common import filter_activities_by_type


class SummaryModel:
    def __init__(self, activities: List[Activity], report_range: DateRange):
        self.report_range = report_range

        working_activities = filter_activities_by_type(activities, Activity.Type.WORK)
        break_activities = filter_activities_by_type(activities, Activity.Type.BREAK)

        self.working_time = duration(working_activities)
        self.break_time = duration(break_activities)

        self.last_activity = activities[-1] if activities else None


def duration(activities: List[Activity]) -> datetime.timedelta:
    return sum((act.duration for act in activities), datetime.timedelta())
