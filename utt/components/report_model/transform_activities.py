import datetime
from typing import Optional

from ...constants import HELLO_ENTRY_NAME
from ...data_structures.activity import Activity
from ..activities import Activities
from ..local_timezone import LocalTimezone
from ..now import Now
from ..report_model.range import ReportRange


def add_current_activity_and_filter_activities(
    activities: Activities,
    current_activity_name: str,
    include_current_activity: bool,
    project_name: Optional[str],
    local_timezone: LocalTimezone,
    now: Now,
    report_range: ReportRange,
):
    add_current_activity(
        activities,
        now,
        current_activity_name,
        include_current_activity,
        report_range.report_range.start,
        report_range.report_range.end,
    )
    activities_ = remove_hello_activities(activities)
    activities_ = filter_activities_by_range(
        activities_, report_range.collect_range.start, report_range.collect_range.end, local_timezone
    )
    activities_ = filter_activities_by_project(activities_, project_name)
    return activities_


def filter_activities_by_range(activities, start_date, end_date, local_timezone):
    start_datetime = local_timezone.localize(datetime.datetime(start_date.year, start_date.month, start_date.day))
    end_datetime = local_timezone.localize(
        datetime.datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59, 99999)
    )

    for full_activity in activities:
        activity = full_activity.clip(start_datetime, end_datetime)
        if activity.duration > datetime.timedelta():
            yield activity


def filter_activities_by_project(activities, project):
    for activity in activities:
        if project is None or project == activity.name.project:
            yield activity


def add_current_activity(
    activities, now, current_activity_name, include_current_activity, report_start_date, report_end_date,
):
    if not activities or not include_current_activity:
        return

    today = now.date()
    report_is_today = today == report_start_date and today == report_end_date
    now_is_after_last_activity = activities[-1].end < now

    if report_is_today and now_is_after_last_activity:
        activities.append(Activity(current_activity_name, activities[-1].end, now, True))


def remove_hello_activities(activities_):
    for activity in activities_:
        if activity.name.name != HELLO_ENTRY_NAME:
            yield activity
