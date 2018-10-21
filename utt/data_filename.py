import os


def data_filename(args, data_dirname):
    if args.data_filename:
        return args.data_filename

    return os.path.join(data_dirname, 'utt.log')
