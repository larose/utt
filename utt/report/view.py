from .activities_section import ActivitiesView
from .details_section import DetailsView
from .projects_section import ProjectsView
from .projects_per_day_section import ProjectsPerDayView
from .summary_section import SummaryView


class ReportView:
    def __init__(self, report):
        self._report = report

    def render(self, output):
        SummaryView(self._report.summary_model).render(output)
        if self._report.args.projects_per_day:
            ProjectsPerDayView(
                self._report.projects_per_day_model).render(output)
        else:
            ProjectsView(self._report.projects_model).render(output)
        ActivitiesView(self._report.activities_model).render(output)
        if self._report.start_date == self._report.end_date:
            DetailsView(self._report.details_model).render(output)
