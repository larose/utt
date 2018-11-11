from __future__ import print_function

from . import formatter
from .common import clip_activities_by_range


class DetailsModel:
    def __init__(self, activities, start_date, end_date, local_timezone):
        self.activities = clip_activities_by_range(start_date, end_date,
                                                   activities, local_timezone)
        self.local_timezone = local_timezone


class DetailsView:
    def __init__(self, model):
        self._model = model

    def render(self, output):
        # Avoid import cycle
        from ..commands import hello

        print(file=output)
        print(formatter.title('Details'), file=output)
        print(file=output)

        for activity in self._model.activities:
            if activity.name.name == hello.HelloCommand.NAME:
                continue
            print(
                "(%s) %s-%s %s" %
                (formatter.format_duration(activity.duration),
                 _format_time(activity.start, self._model.local_timezone),
                 _format_time(activity.end, self._model.local_timezone),
                 activity.name),
                file=output)

        print(file=output)


# pylint: disable=redefined-outer-name
def _format_time(datetime, local_timezone):
    return datetime.astimezone(local_timezone).strftime("%H:%M")
