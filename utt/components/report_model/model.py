from ...report.activities.model import ActivitiesModel
from ...report.details.model import DetailsModel
from ...report.per_day.model import PerDayModel
from ...report.projects.model import ProjectsModel
from ...report.summary.model import SummaryModel
from ..activities import Activities
from ..report_args import ReportArgs


def report(report_args: ReportArgs, filtered_activities: Activities):
    return ReportModel(activities=filtered_activities, args=report_args)


class ReportModel:
    def __init__(self, activities: Activities, args: ReportArgs):
        self.args = args
        self.summary_model = SummaryModel(activities, args.range)
        self.projects_model = ProjectsModel(activities)
        self.per_day_model = PerDayModel(activities)
        self.activities_model = ActivitiesModel(activities)
        self.details_model = DetailsModel(activities)
