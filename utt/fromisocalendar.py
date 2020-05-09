import datetime
import sys


def date_fromisocalendar(year: int, week: int, day: int) -> datetime.date:
    if sys.version_info >= (3, 8):
        return datetime.date.fromisocalendar(year, week, day)

    return _date_fromisocalendar(year, week, day)


# Source: https://github.com/python/cpython/blob/96b1c59c71534db3f0f3799cd84e2006923a5098/Lib/datetime.py#L32
_DAYS_IN_MONTH = [-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# Source: https://github.com/python/cpython/blob/96b1c59c71534db3f0f3799cd84e2006923a5098/Lib/datetime.py#L34-L39
_DAYS_BEFORE_MONTH = [-1]  # -1 is a placeholder for indexing purposes.
dbm = 0
for dim in _DAYS_IN_MONTH[1:]:
    _DAYS_BEFORE_MONTH.append(dbm)
    dbm += dim
del dbm, dim


# Source: https://github.com/python/cpython/blob/96b1c59c71534db3f0f3799cd84e2006923a5098/Lib/datetime.py#L57-L60
def _days_before_month(year, month):
    "year, month -> number of days in year preceding first day of month."
    assert 1 <= month <= 12, "month must be in 1..12"
    return _DAYS_BEFORE_MONTH[month] + (month > 2 and _is_leap(year))


# Source: https://github.com/python/cpython/blob/96b1c59c71534db3f0f3799cd84e2006923a5098/Lib/datetime.py#L45-L48
def _days_before_year(year):
    "year -> number of days before January 1st of year."
    y = year - 1
    return y * 365 + y // 4 - y // 100 + y // 400


# Source: https://github.com/python/cpython/blob/96b1c59c71534db3f0f3799cd84e2006923a5098/Lib/datetime.py#L71-L73
_DI400Y = _days_before_year(401)  # number of days in 400 years
_DI100Y = _days_before_year(101)  # "    "   "   " 100   "
_DI4Y = _days_before_year(5)  # "    "   "   "   4   "


# Source: https://github.com/python/cpython/blob/96b1c59c71534db3f0f3799cd84e2006923a5098/Lib/datetime.py#L50-L55
def _days_in_month(year, month):
    "year, month -> number of days in that month in that year."
    assert 1 <= month <= 12, month
    if month == 2 and _is_leap(year):
        return 29
    return _DAYS_IN_MONTH[month]


# Source: https://github.com/python/cpython/blob/96b1c59c71534db3f0f3799cd84e2006923a5098/Lib/datetime.py#L41-L43
def _is_leap(year):
    "year -> 1 if leap year, else 0."
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


# Source: https://github.com/python/cpython/blob/96b1c59c71534db3f0f3799cd84e2006923a5098/Lib/datetime.py#L2171-L2180
def _isoweek1monday(year):
    # Helper to calculate the day number of the Monday starting week 1
    # XXX This could be done more efficiently
    THURSDAY = 3
    firstday = _ymd2ord(year, 1, 1)
    firstweekday = (firstday + 6) % 7  # See weekday() above
    week1monday = firstday - firstweekday
    if firstweekday > THURSDAY:
        week1monday += 7
    return week1monday


# Source: https://github.com/python/cpython/blob/96b1c59c71534db3f0f3799cd84e2006923a5098/Lib/datetime.py#L87-L147
def _ord2ymd(n):
    "ordinal -> (year, month, day), considering 01-Jan-0001 as day 1."

    # n is a 1-based index, starting at 1-Jan-1.  The pattern of leap years
    # repeats exactly every 400 years.  The basic strategy is to find the
    # closest 400-year boundary at or before n, then work with the offset
    # from that boundary to n.  Life is much clearer if we subtract 1 from
    # n first -- then the values of n at 400-year boundaries are exactly
    # those divisible by _DI400Y:
    #
    #     D  M   Y            n              n-1
    #     -- --- ----        ----------     ----------------
    #     31 Dec -400        -_DI400Y       -_DI400Y -1
    #      1 Jan -399         -_DI400Y +1   -_DI400Y      400-year boundary
    #     ...
    #     30 Dec  000        -1             -2
    #     31 Dec  000         0             -1
    #      1 Jan  001         1              0            400-year boundary
    #      2 Jan  001         2              1
    #      3 Jan  001         3              2
    #     ...
    #     31 Dec  400         _DI400Y        _DI400Y -1
    #      1 Jan  401         _DI400Y +1     _DI400Y      400-year boundary
    n -= 1
    n400, n = divmod(n, _DI400Y)
    year = n400 * 400 + 1  # ..., -399, 1, 401, ...

    # Now n is the (non-negative) offset, in days, from January 1 of year, to
    # the desired date.  Now compute how many 100-year cycles precede n.
    # Note that it's possible for n100 to equal 4!  In that case 4 full
    # 100-year cycles precede the desired day, which implies the desired
    # day is December 31 at the end of a 400-year cycle.
    n100, n = divmod(n, _DI100Y)

    # Now compute how many 4-year cycles precede it.
    n4, n = divmod(n, _DI4Y)

    # And now how many single years.  Again n1 can be 4, and again meaning
    # that the desired day is December 31 at the end of the 4-year cycle.
    n1, n = divmod(n, 365)

    year += n100 * 100 + n4 * 4 + n1
    if n1 == 4 or n100 == 4:
        assert n == 0
        return year - 1, 12, 31

    # Now the year is correct, and n is the offset from January 1.  We find
    # the month via an estimate that's either exact or one too large.
    leapyear = n1 == 3 and (n4 != 24 or n100 == 3)
    assert leapyear == _is_leap(year)
    month = (n + 50) >> 5
    preceding = _DAYS_BEFORE_MONTH[month] + (month > 2 and leapyear)
    if preceding > n:  # estimate is too large
        month -= 1
        preceding -= _DAYS_IN_MONTH[month] + (month == 2 and leapyear)
    n -= preceding
    assert 0 <= n < _days_in_month(year, month)

    # Now the year and month are correct, and n is the offset from the
    # start of that month:  we're done!
    return year, month, n + 1


# Source: https://github.com/python/cpython/blob/96b1c59c71534db3f0f3799cd84e2006923a5098/Lib/datetime.py#L62-L69
def _ymd2ord(year, month, day):
    "year, month, day -> ordinal, considering 01-Jan-0001 as day 1."
    assert 1 <= month <= 12, "month must be in 1..12"
    dim = _days_in_month(year, month)
    assert 1 <= day <= dim, "day must be in 1..%d" % dim
    return _days_before_year(year) + _days_before_month(year, month) + day


# Source: https://github.com/python/cpython/blob/96b1c59c71534db3f0f3799cd84e2006923a5098/Lib/datetime.py#L891-L924
def _date_fromisocalendar(year, week, day):
    """Construct a date from the ISO year, week number and weekday.
    This is the inverse of the date.isocalendar() function"""
    # Year is bounded this way because 9999-12-31 is (9999, 52, 5)
    if not datetime.MINYEAR <= year <= datetime.MAXYEAR:
        raise ValueError(f"Year is out of range: {year}")

    if not 0 < week < 53:
        out_of_range = True

        if week == 53:
            # ISO years have 53 weeks in them on years starting with a
            # Thursday and leap years starting on a Wednesday
            first_weekday = _ymd2ord(year, 1, 1) % 7
            if first_weekday == 4 or (first_weekday == 3 and _is_leap(year)):
                out_of_range = False

        if out_of_range:
            raise ValueError(f"Invalid week: {week}")

    if not 0 < day < 8:
        raise ValueError(f"Invalid weekday: {day} (range is [1, 7])")

    # Now compute the offset from (Y, 1, 1) in days:
    day_offset = (week - 1) * 7 + (day - 1)

    # Calculate the ordinal day for monday, week 1
    day_1 = _isoweek1monday(year)
    ord_day = day_1 + day_offset

    return datetime.date(*_ord2ymd(ord_day))
