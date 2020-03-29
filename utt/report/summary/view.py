import datetime

from ...components.output import Output
from ...data_structures.activity import Activity
from .. import formatter
from .model import SummaryModel, WorkingBreakTime


class SummaryView:
    def __init__(self, model: SummaryModel):
        self._model = model

    def render(self, output: Output) -> None:
        print(file=output)
        date_str = format_date(self._model.start_date)
        if self._model.end_date != self._model.start_date:
            date_str = " ".join([date_str, "to", format_date(self._model.end_date)])
        print(formatter.title(date_str), file=output)

        print(file=output)
        _print_time(self._model, self._model.working_time, output)
        _print_time(self._model, self._model.break_time, output)


def _print_time(summary_section: SummaryModel, working_break_time: WorkingBreakTime, output: Output,) -> None:
    activity_names = {
        Activity.Type.WORK: "Working Time",
        Activity.Type.BREAK: "Break   Time",
    }

    print(
        "%s: %s"
        % (
            activity_names[working_break_time.activity_type],
            formatter.format_duration(working_break_time.total_duration),
        ),
        end="",
        file=output,
    )

    if (
        summary_section.current_activity is not None
        and summary_section.current_activity.type == working_break_time.activity_type
    ):
        cur_duration = summary_section.current_activity.duration
        print(
            " (%s + %s)"
            % (
                formatter.format_duration(working_break_time.total_duration - cur_duration),
                formatter.format_duration(cur_duration),
            ),
            end="",
            file=output,
        )

    if summary_section.start_date == summary_section.end_date:
        print(
            " [%s]" % formatter.format_duration(working_break_time.weekly_duration), file=output,
        )
    else:
        print(file=output)


def format_date(date: datetime.date) -> str:
    return date.strftime("%A, %b %d, %Y (week {week})".format(week=date.isocalendar()[1]))
