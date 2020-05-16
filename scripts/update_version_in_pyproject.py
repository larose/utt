# License: MIT
# Source: https://github.com/larose/cargo/blob/a8d46de04b38a0847ba7ec60591aed3a4d6eecf5/scripts/update_version_in_pyproject.py
import re
import subprocess
import sys
import typing

UNRELEASED_VERSION_NAME = "(unreleased)"


def get_first_line(changelog_filename: str) -> str:
    with open(changelog_filename) as changelog:
        return changelog.readline().rstrip("\n")


def get_version(changelog_filename: str) -> typing.Optional[str]:
    first_line = get_first_line(changelog_filename)
    print(f"Changelog first line: {first_line}")
    return parse_version_from_line(first_line)


def parse_version_from_line(line: str) -> str:
    if line == f"## {UNRELEASED_VERSION_NAME}":
        return UNRELEASED_VERSION_NAME

    # Example: ## 1.0 (2020-08-25)
    match = re.match(r"## (?P<version>[^\s(]+) \(\d{4}-\d{2}-\d{2}\)", line)
    if match is None:
        raise Exception(f"Invalid line: {line}")

    return match.group("version")


def main():
    changelog_filename = sys.argv[1]
    print(f"Changelog filename: {changelog_filename}")

    version = get_version(changelog_filename)
    print(f"Version: {version}")

    if version == UNRELEASED_VERSION_NAME:
        version = "0"

    print(
        subprocess.check_output(
            ["poetry", "version", version], stderr=sys.stderr
        ).decode()
    )


if __name__ == "__main__":
    main()
