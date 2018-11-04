from .activities_section import ActivitiesModel
from .details_section import DetailsModel
from .projects_section import ProjectsModel
from .summary_section import SummaryModel


class Report:
    def __init__(self, activities, start_date, end_date, local_timezone):
        self.summary_model = SummaryModel(activities, start_date, end_date,
                                          local_timezone)
        self.projects_model = ProjectsModel(activities, start_date, end_date,
                                            local_timezone)
        self.activities_model = ActivitiesModel(activities, start_date,
                                                end_date, local_timezone)
        self.details_model = DetailsModel(activities, start_date, end_date,
                                          local_timezone)
        self.start_date = start_date
        self.end_date = end_date
