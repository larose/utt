from .activities_section import ActivitiesView
from .details_section import DetailsView
from .projects_section import ProjectsView
from .per_day_section import PerDayView
from .summary_section import SummaryView


class ReportView:
    def __init__(self, report):
        self._report = report

    def render(self, output):
        SummaryView(self._report.summary_model).render(output)
        if self._report.args.per_day:
            PerDayView(self._report.per_day_model).render(output)
        else:
            ProjectsView(self._report.projects_model).render(output)
        ActivitiesView(self._report.activities_model).render(output)
        if self._report.start_date == self._report.end_date:
            DetailsView(self._report.details_model).render(output)

    def csv(self, section, output):
        if section == 'summary':
            view = SummaryView(self._report.summary_model)
        elif section == 'per_day':
            view = PerDayView(self._report.per_day_model)
        elif section == 'projects':
            view = ProjectsView(self._report.projects_model)
        elif section == 'activities':
            view = ActivitiesView(self._report.activities_model)
        elif section == 'details':
            view = DetailsView(self._report.details_model)
        else:
            view = None

        if not hasattr(view, 'csv'):
            raise ValueError(
                f"CSV output not yet implemented for '{section}' section")
        view.csv(output)
