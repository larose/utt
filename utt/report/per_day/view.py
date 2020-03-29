from __future__ import print_function

import csv

from utt.components.output import Output
from utt.report import formatter
from utt.report.per_day.model import PerDayModel

from .common import timedelta_to_billable


class PerDayView:
    def __init__(self, model: PerDayModel):
        self._model = model

    def render(self, output: Output) -> None:
        print(file=output)
        print(formatter.title("Per Day"), file=output)
        print(file=output)

        fmt = "{date}: {hours}h {duration:>7} - {projects} - {tasks}"
        for date_activities in self._model.dates:
            date_render = fmt.format(
                date=date_activities["date"].isoformat(),
                hours=timedelta_to_billable(date_activities["hours"]),
                duration="({duration})".format(duration=date_activities["duration"]),
                projects=date_activities["projects"],
                tasks=date_activities["tasks"],
            )
            print(date_render, file=output)

    def csv(self, output: Output) -> None:
        if not self._model.dates:
            print(" -- No activities for this time range --", file=output)
            return

        fieldnames = ["date", "hours", "duration", "projects", "tasks"]
        writer = csv.DictWriter(output, fieldnames=fieldnames)

        # Write header
        writer.writerow({fn: fn.capitalize() for fn in fieldnames})

        for date_activities in self._model.dates:
            date_activities["hours"] = timedelta_to_billable(date_activities["hours"]).strip()
            writer.writerow(date_activities)
