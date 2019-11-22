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
        print(file=output)
        print(formatter.title('Details'), file=output)
        print(file=output)

        # Print date only when the activities have different dates.
        if not self._model.activities:
            print_date = False
        else:
            print_date = (self._model.activities[0].start.date() !=
                          self._model.activities[-1].start.date())
        current_date = None
        for activity in self._model.activities:
            if print_date and current_date != activity.start.date():
                if current_date is not None:
                    print("", file=output)
                current_date = activity.start.date()
                print("{}:".format(current_date.isoformat()), file=output)
                print("", file=output)
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
