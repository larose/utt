from utt.report.details.view import DetailsView
from utt.report.per_day.view import PerDayView

from ..components.output import Output
from ..components.report_args import CSVSection
from ..components.report_model import ReportModel


class CSVReportView:
    def __init__(self, report: ReportModel):
        self._report = report

    def render(self, output: Output) -> None:
        section = self._report.args.csv_section

        if section == CSVSection.per_day:
            PerDayView(self._report.per_day_model).csv(output)
        if section == CSVSection.per_task:
            DetailsView(self._report.details_model).csv(output)
