def config(config_filename, default_config):
    config = default_config()
    config.read(config_filename)
    return config
