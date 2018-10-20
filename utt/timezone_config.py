import tzlocal


class TimezoneConfig:
    def __init__(self):
        self._local_timezone = None

    def enabled(self):
        return False

    def local_timezone(self):
        if self._local_timezone is None:
            self._local_timezone = tzlocal.get_localzone()

        return self._local_timezone


def timezone_config():
    return TimezoneConfig()
