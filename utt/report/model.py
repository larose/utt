import argparse
from datetime import date
from typing import List

from pytz.tzinfo import DstTzInfo

from ..data_structures.activity import Activity
from .activities_section import ActivitiesModel
from .details_section import DetailsModel
from .per_day_section import PerDayModel
from .projects_section import ProjectsModel
from .summary_section import SummaryModel


class Report:
    def __init__(
        self,
        activities: List[Activity],
        start_date: date,
        end_date: date,
        local_timezone: DstTzInfo,
        args: argparse.Namespace,
    ):
        self.summary_model = SummaryModel(activities, start_date, end_date, local_timezone)
        self.projects_model = ProjectsModel(activities, start_date, end_date, local_timezone)
        self.per_day_model = PerDayModel(activities, start_date, end_date, local_timezone)
        self.activities_model = ActivitiesModel(activities, start_date, end_date, local_timezone)
        self.details_model = DetailsModel(activities, start_date, end_date, local_timezone)
        self.start_date = start_date
        self.end_date = end_date
        self.args = args
