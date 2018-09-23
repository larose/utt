import datetime

_ZERO_DT = datetime.timedelta(0)


class TimezoneOffset(datetime.tzinfo):
    """Fixed offset in minutes east from UTC."""

    def __init__(self, offset=0, name=None):
        self._offset = datetime.timedelta(minutes=offset)
        self._name = name

    def utcoffset(self, dt):
        return self._offset

    def tzname(self, dt):
        return self._name

    def dst(self, dt):
        return _ZERO_DT

    @classmethod
    def from_string(cls, offset_str):
        """ Parse UTC Offset in string format.

        Parameters
        ----------
        offset_str : str
            Must have the format of +HH:MM or -HH:MM or +HHMM or -HHMM
        """
        sign = {"+": 1, "-": -1}[offset_str[0]]
        offset_str = offset_str.replace(":", "")
        hours = int(offset_str[1:3])
        minutes = int(offset_str[3:5])
        offset = (hours * 60 + minutes) * sign
        return cls(offset=offset)
