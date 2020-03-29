import argparse
from datetime import date
from enum import Enum, auto
from typing import Optional

from pytz.tzinfo import DstTzInfo

from ...report.activities.model import ActivitiesModel
from ...report.details.model import DetailsModel
from ...report.per_day.model import PerDayModel
from ...report.projects.model import ProjectsModel
from ...report.summary.model import SummaryModel
from ..activities import Activities
from ..local_timezone import LocalTimezone
from ..now import Now
from ..report_model.range import parse_report_range_arguments
from ..report_model.transform_activities import add_current_activity_and_filter_activities


class CSVSection(Enum):
    per_day = auto()


csv_section_name_to_csv_section = {"per-day": CSVSection.per_day, "per_day": CSVSection.per_day}


def report(args: argparse.Namespace, now: Now, activities: Activities, local_timezone: LocalTimezone):
    report_range = parse_report_range_arguments(
        unparsed_report_date=args.report_date,
        unparsed_month=args.month,
        unparsed_week=args.week,
        unparsed_from_date=args.from_date,
        unparsed_to_date=args.to_date,
        today=now.date(),
    )

    activities_ = add_current_activity_and_filter_activities(
        activities=activities.copy(),
        current_activity_name=args.current_activity,
        include_current_activity=not args.no_current_activity,
        project_name=args.project,
        local_timezone=local_timezone,
        now=now,
        report_range=report_range,
    )

    return ReportModel(
        activities=list(activities_),
        start_date=report_range.report_range.start,
        end_date=report_range.report_range.end,
        local_timezone=local_timezone,
        csv_section=csv_section_name_to_csv_section.get(args.csv_section),
        per_day=args.per_day,
        show_details=args.details,
        show_comments=args.comments,
    )


class ReportModel:
    def __init__(
        self,
        activities: Activities,
        start_date: date,
        end_date: date,
        local_timezone: DstTzInfo,
        csv_section: Optional[CSVSection],
        per_day: bool,
        show_details: bool,
        show_comments: bool,
    ):
        self.summary_model = SummaryModel(activities, start_date, end_date, local_timezone)
        self.projects_model = ProjectsModel(activities, start_date, end_date, local_timezone)
        self.per_day_model = PerDayModel(activities, start_date, end_date, local_timezone)
        self.activities_model = ActivitiesModel(activities, start_date, end_date, local_timezone)
        self.details_model = DetailsModel(activities, start_date, end_date, local_timezone)
        self.start_date = start_date
        self.end_date = end_date
        self.csv_section = csv_section
        self.per_day = per_day
        self.show_details = show_details
        self.show_comments = show_comments
