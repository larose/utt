import datetime


def timedelta_to_billable(time_delta: datetime.timedelta) -> str:
    """Ad hoc method for rounding a decimal number of hours to "billable"

    Round to the nearest 6 minutes / 0.1 hours.  This means that 2,
    8, 14 minutes should get rounded down and 3, 9, 15 minutes
    should get rounded up.

    Note that Python's standard rounding function round() uses
    what's referred to as "banker's rounding".  We fix it by adding
    0.000001 (1e-6), or less than 4 milliseconds.

    Alternative would be to use the Decimal module, for instance as
    suggested here: https://stackoverflow.com/a/33019948/3061818
    """
    hours = time_delta.total_seconds() / (60 * 60)
    # Round to nearest 6 minutes (0.1h), rounding up 3, 9, 15 mins (etc.)
    hours += 0.000001  # Hack to avoid 'banker's rounding.
    hours = round(hours * 10) / 10
    return "{hours:4.1f}".format(hours=hours)
