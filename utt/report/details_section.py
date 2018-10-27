from __future__ import print_function
from .common import clip_activities_by_range
from . import formatter


class DetailsModel:
    def __init__(self, activities, start_date, end_date):
        self.activities = clip_activities_by_range(start_date, end_date,
                                                   activities)


class DetailsView:
    def __init__(self, model):
        self._model = model

    def render(self, output):
        print(file=output)
        print(formatter.title('Details'), file=output)
        print(file=output)

        for activity in self._model.activities:
            print(
                "(%s) %s-%s %s" % (formatter.format_duration(
                    activity.duration), _format_time(activity.start),
                                   _format_time(activity.end), activity.name),
                file=output)

        print(file=output)


# pylint: disable=redefined-outer-name
def _format_time(datetime):
    return datetime.strftime("%H:%M")
