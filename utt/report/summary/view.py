import datetime

from ...components.output import Output
from ...data_structures.activity import Activity
from .. import formatter
from .model import SummaryModel


class SummaryView:
    def __init__(self, model: SummaryModel):
        self._model = model

    def render(self, output: Output) -> None:
        print(file=output)
        date_str = format_date(self._model.report_range.start)
        if self._model.report_range.start != self._model.report_range.end:
            date_str = " ".join([date_str, "to", format_date(self._model.report_range.end)])
        print(formatter.title(date_str), file=output)

        print(file=output)
        _print_time(self._model, self._model.working_time, Activity.Type.WORK, "Working Time", output)
        _print_time(self._model, self._model.break_time, Activity.Type.BREAK, "Break   Time", output)


# working_break_time: duration
def _print_time(
    model: SummaryModel, working_break_time, activity_type: Activity.Type, activity_name: str, output: Output,
) -> None:
    print(
        "%s: %s" % (activity_name, formatter.format_duration(working_break_time),), end="", file=output,
    )

    if (
        model.last_activity is not None
        and model.last_activity.is_current_activity
        and model.last_activity.type == activity_type
    ):
        cur_duration = model.last_activity.duration
        print(
            " (%s + %s)"
            % (formatter.format_duration(working_break_time - cur_duration), formatter.format_duration(cur_duration),),
            end="",
            file=output,
        )

    print(file=output)


def format_date(date: datetime.date) -> str:
    return date.strftime("%A, %b %d, %Y (week {week})".format(week=date.isocalendar()[1]))
