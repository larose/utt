class TimezoneConfig:
    def __init__(self, enabled):
        self._enabled = enabled

    def enabled(self):
        return self._enabled


def timezone_config(config):
    enabled = config.getboolean('timezone', 'enabled')
    return TimezoneConfig(enabled)
