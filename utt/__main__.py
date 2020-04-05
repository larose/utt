from .check_python_version import warn_if_python_version_is_unsupported

warn_if_python_version_is_unsupported()


def main():
    from utt.main import main

    main()


if __name__ == "__main__":
    main()
