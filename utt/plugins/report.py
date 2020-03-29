import argparse

from ..api import _v1
from ..components.report_model import ReportModel, csv_section_name_to_csv_section
from ..report.view import ReportView  # Private API


class ReportHandler:
    def __init__(self, report_model: ReportModel, output: _v1.Output):
        self._report = report_model
        self._output = output

    def __call__(self):
        view = ReportView(self._report)
        view.render(self._output)


def add_args(parser: argparse.ArgumentParser):
    parser.add_argument("report_date", metavar="date", type=str, nargs="?")

    parser.add_argument(
        "--current-activity", default="-- Current Activity --", type=str, help="Set the current activity",
    )

    parser.add_argument(
        "--no-current-activity", action="store_true", default=False, help="Do not display the current activity",
    )

    parser.add_argument(
        "--from", default=None, dest="from_date", type=str, help="Specify an inclusive start date to report.",
    )

    parser.add_argument(
        "--to",
        default=None,
        dest="to_date",
        type=str,
        help=(
            "Specify an inclusive end date to report. "
            "If this is a day of the week, then it is the next occurrence "
            "from the start date of the report, including the start date "
            "itself."
        ),
    )

    parser.add_argument(
        "--project", default=None, type=str, help="Show activities only for the specified project.",
    )

    parser.add_argument(
        "--per-day", action="store_true", default=False, help="Show total hours per day.",
    )

    parser.add_argument(
        "--csv-section",
        choices=list(csv_section_name_to_csv_section.keys()),
        default=None,
        help="Instead of text output, print CSV of desired section",
    )

    parser.add_argument(
        "--month",
        default=None,
        nargs="?",
        const="this",
        type=str,
        help=(
            "Specify a month. "
            "Allowed formats include, '2019-10', 'Oct', 'this' 'prev'. "
            "The report will start on the first day of the month and end "
            "on the last.  '--from' or '--to' if present will override "
            "start and end, respectively.  If the month is the current "
            "month, 'today' will be the last day of the report."
        ),
    )

    parser.add_argument(
        "--week",
        default=None,
        nargs="?",
        const="this",
        type=str,
        help=(
            "Specify a week. "
            "Allowed formats include, 'this' 'prev', or week noumber. "
            "The report will start on the first day of the week (Monday) "
            "and end on the last (Sunday).  '--from' or '--to' if present "
            "will override start and end, respectively.  If the week is "
            "the current week, 'today' will be the last day of the report."
        ),
    )

    parser.add_argument(
        "--details", action="store_true", default=False, help="Show details even for multi-day reports.",
    )

    parser.add_argument(
        "--comments", action="store_true", default=False, help="Show comments in details sections.",
    )


report_command = _v1.Command("report", "Summarize tasks for given time period", ReportHandler, add_args)

_v1.add_command(report_command)
