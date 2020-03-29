import csv

from ...components.output import Output
from .common import timedelta_to_billable
from .model import PerDayModel


class CSVPerDayView:
    def __init__(self, model: PerDayModel):
        self._model = model

    def render(self, output: Output) -> None:
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
