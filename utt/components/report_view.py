from utt.components.output import Output
from utt.components.report_model import ReportModel
from utt.report.activities_section import ActivitiesView
from utt.report.details_section import DetailsView
from utt.report.per_day.view import PerDayView
from utt.report.projects_section import ProjectsView
from utt.report.summary_section import SummaryView


class ReportView:
    def __init__(self, report: ReportModel):
        self._report = report

    def render(self, output: Output) -> None:
        SummaryView(self._report.summary_model).render(output)

        if self._report.per_day:
            PerDayView(self._report.per_day_model).render(output)
        else:
            ProjectsView(self._report.projects_model).render(output)

        ActivitiesView(self._report.activities_model).render(output)

        if (self._report.start_date == self._report.end_date) or self._report.show_details:
            DetailsView(self._report.details_model, show_comments=self._report.show_comments).render(output)
