from .summary_section import SummaryModel
from .projects_section import ProjectsModel
from .activities_section import ActivitiesModel
from .details_section import DetailsModel


class Report:
    def __init__(self, activities, start_date, end_date):
        self.summary_model = SummaryModel(activities, start_date, end_date)
        self.projects_model = ProjectsModel(activities, start_date, end_date)
        self.activities_model = ActivitiesModel(activities, start_date,
                                                end_date)
        self.details_model = DetailsModel(activities, start_date, end_date)
        self.start_date = start_date
        self.end_date = end_date
