from __future__ import print_function

import datetime
import itertools
import math
import csv

from . import formatter
from ..activity import Activity
from .common import (clip_activities_by_range, filter_activities_by_type,
                     print_dicts)


class PerDayModel:
    def __init__(self, activities, start_date, end_date, local_timezone):
        activities = clip_activities_by_range(start_date, end_date, activities,
                                              local_timezone)

        self.dates = _groupby_date(
            filter_activities_by_type(activities, Activity.Type.WORK))


class PerDayView:
    def __init__(self, model):
        self._model = model

    @staticmethod
    def _timedelta_to_billable(td):
        """Ad hoc method for rounding a decimal number of hours to "billable"

        Using the following approach: round up to the nearest 6 minutes
        (10th of an hour).
        """
        hours = td.total_seconds() / (60 * 60)
        # Round up to nearest 6 minutes
        rounder = math.ceil  # Replace with 'round' if that's more appropriate
        hours = rounder(hours * 10) / 10
        return f"{hours:4.1f}"

    def render(self, output):
        print(file=output)
        print(formatter.title('Per Day'), file=output)
        print(file=output)

        fmt = "{date}: {hours} {duration:>7} - {projects} - {tasks}"
        for date_activities in self._model.dates:
            date_render = fmt.format(
                date=date_activities['date'].isoformat(),
                hours=self._timedelta_to_billable(date_activities['hours']),
                duration=f"({date_activities['duration']})",
                projects=date_activities['projects'],
                tasks=date_activities['tasks'],
            )
            print(date_render, file=output)

    def csv(self, output):
        print("CSV output will come here", file=output)
        fieldnames = ['date', 'hours', 'duration', 'projects', 'tasks']
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        # Write header
        writer.writerow({fn: fn.capitalize() for fn in fieldnames})
        for date_activities in self._model.dates:
            date_activities['hours'] = self._timedelta_to_billable(
                date_activities['hours']).strip()
            writer.writerow(date_activities)


def _groupby_date(activities):
    def key(act):
        """Key on date."""
        return act.start.date()

    result = []
    sorted_activities = sorted(activities, key=key)
    # pylint: disable=redefined-argument-from-local
    for date, activities in itertools.groupby(sorted_activities, key):
        activities = list(activities)
        duration = sum((act.duration for act in activities),
                       datetime.timedelta())
        result.append({
            'duration':
            formatter.format_duration(duration),
            'hours':
            duration,
            'date':
            date,
            'projects':
            ", ".join(
                sorted(
                    set(act.name.project for act in activities),
                    key=lambda project: project.lower())),
            'tasks':
            ", ".join(
                sorted(
                    set(act.name.task for act in activities),
                    key=lambda task: task.lower()))
        })

    return sorted(result, key=lambda result: result['date'])
