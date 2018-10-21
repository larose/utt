import os


def config_dirname():
    base_dir_name = os.getenv('XDG_DATA_CONFIG',
                              os.path.expanduser("~/.config"))

    return os.path.join(base_dir_name, 'utt')
