import datetime
from typing import List, Optional

from pytz.tzinfo import DstTzInfo

from ...data_structures.activity import Activity
from ..common import clip_activities_by_range, filter_activities_by_type


class WorkingBreakTime:
    def __init__(
        self,
        activity_type: Activity.Type,
        activities: List[Activity],
        start_date: datetime.date,
        end_date: datetime.date,
        local_timezone: DstTzInfo,
    ):
        self.activity_type = activity_type

        self.total_duration = duration(clip_activities_by_range(start_date, end_date, activities, local_timezone))

        self.weekly_duration = duration(activities)


class SummaryModel:
    def __init__(
        self, activities: List[Activity], start_date: datetime.date, end_date: datetime.date, local_timezone: DstTzInfo,
    ):
        self.start_date = start_date
        self.end_date = end_date

        working_activities = filter_activities_by_type(activities, Activity.Type.WORK)
        break_activities = filter_activities_by_type(activities, Activity.Type.BREAK)

        self.working_time = WorkingBreakTime(
            Activity.Type.WORK, working_activities, start_date, end_date, local_timezone
        )
        self.break_time = WorkingBreakTime(Activity.Type.BREAK, break_activities, start_date, end_date, local_timezone)

        self.current_activity = self._current_activity(activities, local_timezone)

    def _current_activity(self, activities: List[Activity], local_timezone: DstTzInfo) -> Optional[Activity]:
        activities = clip_activities_by_range(self.start_date, self.end_date, activities, local_timezone)

        if not activities:
            return None

        last_activity = activities[-1]
        return last_activity if last_activity.is_current_activity else None


def duration(activities: List[Activity]) -> datetime.timedelta:
    return sum((act.duration for act in activities), datetime.timedelta())
