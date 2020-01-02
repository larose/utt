import os


def data_dirname():
    base_data_dir_name = os.getenv('XDG_DATA_HOME',
                                   os.path.expanduser("~/.local/share"))

    return os.path.join(base_data_dir_name, 'utt')
