from utt.report.per_day.view import PerDayView

from ..components.output import Output
from ..components.report_model import ReportModel
from ..components.report_model.model import CSVSection


class CSVReportView:
    def __init__(self, report: ReportModel):
        self._report = report

    def render(self, output: Output) -> None:
        section = self._report.csv_section

        if section == CSVSection.per_day:
            PerDayView(self._report.per_day_model).csv(output)
