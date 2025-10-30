import argparse

from ..api import _v1


class ProjectSummaryHandler:
    def __init__(self, report_model: _v1._private.ReportModel, output: _v1.Output):
        self._report = report_model
        self._output = output

    def __call__(self):
        view = _v1.ProjectSummaryView(self._report.project_summary_model)
        view.render(self._output)


def add_args(parser: argparse.ArgumentParser):
    parser.add_argument("report_date", metavar="date", type=str, nargs="?")
    parser.set_defaults(csv_section=None, comments=False, details=False, per_day=False)

    parser.add_argument(
        "--current-activity",
        default="-- Current Activity --",
        type=str,
        help="Set the current activity",
    )

    parser.add_argument(
        "--no-current-activity",
        action="store_true",
        default=False,
        help="Do not display the current activity",
    )

    parser.add_argument(
        "--from",
        default=None,
        dest="from_date",
        type=str,
        help="Specify an inclusive start date to report.",
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
        "--project",
        default=None,
        type=str,
        help="Show activities only for the specified project.",
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
            "Allowed formats include, 'this' 'prev', or week number. "
            "The report will start on the first day of the week (Monday) "
            "and end on the last (Sunday).  '--from' or '--to' if present "
            "will override start and end, respectively.  If the week is "
            "the current week, 'today' will be the last day of the report."
        ),
    )


project_summary_command = _v1.Command(
    "project-summary", "Show projects sorted by time spent", ProjectSummaryHandler, add_args
)

_v1.register_command(project_summary_command)
