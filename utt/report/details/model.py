from typing import List

from pytz.tzinfo import DstTzInfo

from utt.data_structures.activity import Activity


class DetailsModel:
    def __init__(
        self, activities: List[Activity], local_timezone: DstTzInfo,
    ):
        self.activities = activities
        self.local_timezone = local_timezone
