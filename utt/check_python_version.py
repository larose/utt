import sys

MIN_PYTHON_VERSION = (3, 7)


def python_version_is_supported():
    python_version = (sys.version_info.major, sys.version_info.minor)

    return python_version >= MIN_PYTHON_VERSION


def warn_if_python_version_is_unsupported():
    if python_version_is_supported():
        return

    print("Warning: utt requires Python version 3.7 or above.", file=sys.stderr)
    print(file=sys.stderr)
