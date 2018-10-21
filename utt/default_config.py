try:
    import configparser
except ImportError:
    import ConfigParser as configparser

DEFAULTS = {'timezone': {'enabled': 'false'}}


class DefaultConfig:
    def __init__(self):
        pass

    def __call__(self):
        config = configparser.ConfigParser()

        for section, options in DEFAULTS.items():
            config.add_section(section)

            for option, value in options.items():
                config.set(section, option, value)

        return config
