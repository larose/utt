from utt.api import _v1


class DefaultReportView(_v1.ReportView):
    def __init__(self, report: _v1.ReportModel):
        self._report = report

    def render(self, output: _v1.Output) -> None:
        _v1.SummaryView(self._report.summary_model).render(output)

        if self._report.per_day:
            _v1.PerDayView(self._report.per_day_model).render(output)
        else:
            _v1.ProjectsView(self._report.projects_model).render(output)

        _v1.ActivitiesView(self._report.activities_model).render(output)

        if (self._report.start_date == self._report.end_date) or self._report.show_details:
            _v1.DetailsView(self._report.details_model, show_comments=self._report.show_comments).render(output)


_v1.register_component(_v1.ReportView, DefaultReportView)
