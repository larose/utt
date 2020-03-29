from datetime import date
from typing import List

from pytz.tzinfo import DstTzInfo

from utt.data_structures.activity import Activity
from utt.report.common import clip_activities_by_range


class DetailsModel:
    def __init__(
        self, activities: List[Activity], start_date: date, end_date: date, local_timezone: DstTzInfo,
    ):
        self.activities = clip_activities_by_range(start_date, end_date, activities, local_timezone)
        self.local_timezone = local_timezone
