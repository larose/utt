from __future__ import print_function

import datetime

from . import formatter
from ..activity import Activity
from .common import clip_activities_by_range, filter_activities_by_type


class WorkingBreakTime:
    # pylint: disable=too-many-arguments
    def __init__(self, activity_type, activities, start_date, end_date,
                 local_timezone):
        self.activity_type = activity_type

        self.total_duration = _duration(
            clip_activities_by_range(start_date, end_date, activities,
                                     local_timezone))

        self.weekly_duration = _duration(activities)


class SummaryModel:
    def __init__(self, activities, start_date, end_date, local_timezone):
        self.start_date = start_date
        self.end_date = end_date

        working_activities = filter_activities_by_type(activities,
                                                       Activity.Type.WORK)
        break_activities = filter_activities_by_type(activities,
                                                     Activity.Type.BREAK)

        self.working_time = WorkingBreakTime(Activity.Type.WORK,
                                             working_activities, start_date,
                                             end_date, local_timezone)
        self.break_time = WorkingBreakTime(Activity.Type.BREAK,
                                           break_activities, start_date,
                                           end_date, local_timezone)

        self.current_activity = self._current_activity(activities,
                                                       local_timezone)

    def _current_activity(self, activities, local_timezone):
        activities = clip_activities_by_range(self.start_date, self.end_date,
                                              activities, local_timezone)

        if not activities:
            return None

        last_activity = activities[-1]
        return last_activity if last_activity.is_current_activity else None


class SummaryView:
    def __init__(self, model):
        self._model = model

    def render(self, output):
        print(file=output)
        date_str = _format_date(self._model.start_date)
        if self._model.end_date != self._model.start_date:
            date_str = " ".join(
                [date_str, "to",
                 _format_date(self._model.end_date)])
        print(formatter.title(date_str), file=output)

        print(file=output)
        _print_time(self._model, self._model.working_time, output)
        _print_time(self._model, self._model.break_time, output)


def _print_time(summary_section, working_break_time, output):
    activity_names = {
        Activity.Type.WORK: 'Working Time',
        Activity.Type.BREAK: 'Break   Time',
    }

    print(
        "%s: %s" % (activity_names[working_break_time.activity_type],
                    formatter.format_duration(
                        working_break_time.total_duration)),
        end='',
        file=output)

    if summary_section.current_activity is not None and \
       summary_section.current_activity.type == working_break_time.activity_type:
        cur_duration = summary_section.current_activity.duration
        print(
            " (%s + %s)" % (formatter.format_duration(
                working_break_time.total_duration - cur_duration),
                            formatter.format_duration(cur_duration)),
            end='',
            file=output)

    if summary_section.start_date == summary_section.end_date:
        print(
            " [%s]" % formatter.format_duration(
                working_break_time.weekly_duration),
            file=output)
    else:
        print(file=output)


def _duration(activities):
    return sum((act.duration for act in activities), datetime.timedelta())


# pylint: disable=redefined-outer-name
def _format_date(datetime):
    return datetime.strftime(
        "%A, %b %d, %Y (week {week})".format(week=datetime.isocalendar()[1]))
