import configparser


class TimezoneConfig:
    def __init__(self, enabled):
        self._enabled = enabled

    def enabled(self):
        return self._enabled


def timezone_config(config: configparser.ConfigParser) -> TimezoneConfig:
    enabled = config.getboolean("timezone", "enabled")
    return TimezoneConfig(enabled)
