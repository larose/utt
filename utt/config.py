def config(config_filename, default_config):
    conf = default_config()
    conf.read(config_filename)
    return conf
