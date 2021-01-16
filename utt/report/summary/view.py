import datetime
from typing import Optional

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

        current_activity_duration = None
        current_activity_type = None

        if self._model.last_activity and self._model.last_activity.is_current_activity:
            current_activity_duration = self._model.last_activity.duration
            current_activity_type = self._model.last_activity.type

        _print_time(self._model, self._model.total_time, "  Total", current_activity_duration, output)
        _print_time(
            self._model,
            self._model.working_time,
            "Working",
            current_activity_duration if current_activity_type == Activity.Type.WORK else None,
            output,
        )
        _print_time(
            self._model,
            self._model.break_time,
            "  Break",
            current_activity_duration if current_activity_type == Activity.Type.BREAK else None,
            output,
        )


def _print_time(
    model: SummaryModel,
    duration: datetime.timedelta,
    activity_name: str,
    current_activity_duration: Optional[datetime.timedelta],
    output: Output,
) -> None:
    print(
        "%s: %s" % (activity_name, formatter.format_duration(duration),), end="", file=output,
    )

    if current_activity_duration:
        print(
            " (%s + %s)"
            % (
                formatter.format_duration(duration - current_activity_duration),
                formatter.format_duration(current_activity_duration),
            ),
            end="",
            file=output,
        )

    print(file=output)


def format_date(date: datetime.date) -> str:
    return date.strftime("%A, %b %d, %Y (week {week})".format(week=date.isocalendar()[1]))
