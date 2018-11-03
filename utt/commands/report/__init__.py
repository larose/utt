import datetime

from .print_report import print_report


class ReportHandler:
    def __init__(self, report, output):
        self._report = report
        self._output = output

    def __call__(self):
        print_report(self._report, self._output)


class ReportCommand:
    NAME = 'report'
    DESCRIPTION = 'Summarize tasks for given time period'

    Handler = ReportHandler

    @staticmethod
    def add_args(parser):
        parser.add_argument("report_date", metavar="date", type=str, nargs='?')

        parser.add_argument(
            "--current-activity",
            default='-- Current Activity --',
            type=str,
            help="Set the current activity")

        parser.add_argument(
            "--no-current-activity",
            action='store_true',
            default=False,
            help="Do not display the current activity")

        parser.add_argument(
            "--from",
            default=None,
            dest="from_date",
            type=str,
            help="Specify an inclusive start date to report.")

        parser.add_argument(
            "--to",
            default=None,
            dest="to_date",
            type=str,
            help="Specify an inclusive end date to report.")


Command = ReportCommand
