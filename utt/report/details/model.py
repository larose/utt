from typing import List

from utt.data_structures.activity import Activity


class DetailsModel:
    def __init__(self, activities: List[Activity]):
        self.activities = activities
