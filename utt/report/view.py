from ..components.output import Output
from ..components.report_model import CSVSection, ReportModel
from .activities_section import ActivitiesView
from .details_section import DetailsView
from .per_day_section import PerDayView
from .projects_section import ProjectsView
from .summary_section import SummaryView


class ReportView:
    def __init__(self, report: ReportModel):
        self._report = report

    def render(self, output: Output):
        if self._report.csv_section:
            self._render_csv(output)
        else:
            self._render_human_readable(output)

    def _render_human_readable(self, output: Output) -> None:
        SummaryView(self._report.summary_model).render(output)
        if self._report.per_day:
            PerDayView(self._report.per_day_model).render(output)
        else:
            ProjectsView(self._report.projects_model).render(output)
        ActivitiesView(self._report.activities_model).render(output)
        if (self._report.start_date == self._report.end_date) or (self._report.show_details):
            DetailsView(self._report.details_model, show_comments=self._report.show_comments).render(output)

    def _render_csv(self, output: Output) -> None:
        section = self._report.csv_section

        if section == CSVSection.per_day:
            PerDayView(self._report.per_day_model).csv(output)
