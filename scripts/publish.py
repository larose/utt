# License: MIT
# Source: https://github.com/larose/cargo/blob/a8d46de04b38a0847ba7ec60591aed3a4d6eecf5/scripts/publish.py
from __future__ import annotations

import subprocess
import sys
import typing

import requests


class PackageInfo(typing.NamedTuple):
    name: str
    version: str

    @staticmethod
    def from_poetry_version_output(poetry_version_output: str) -> PackageInfo:
        name, version = poetry_version_output.rsplit(" ", 1)
        return PackageInfo(name=name, version=version)


def publish(repo_name: str):
    print(f"Publishing...")
    try:

        subprocess.check_call(
            ["poetry", "publish", "-vvv", "-n", "-r", repo_name],
            stdout=sys.stdout,
            stderr=sys.stderr,
        )
    except subprocess.CalledProcessError:
        sys.exit(1)


def tag(package_version):
    tag_name = f"v{package_version}"

    subprocess.check_call(["git", "tag", tag_name], stdout=sys.stdout, stderr=sys.stderr)

    subprocess.check_call(["git", "push", "origin", tag_name], stdout=sys.stdout, stderr=sys.stderr)


def check_version_already_published(repository_url, package_name, version):
    package_metadata_url = f"{repository_url}/{package_name}/{version}/json"
    package_metadata_response = requests.get(package_metadata_url)

    print(f"{package_metadata_url} returned {package_metadata_response.status_code}")

    return package_metadata_response.status_code == 200


def main():
    repo_name = sys.argv[1]
    repo_json_api_url = sys.argv[2]

    print(f"Repository name: {repo_name}")
    print(f"Repository JSON API URL: {repo_json_api_url}")

    poetry_version_output = subprocess.check_output(["poetry", "version", "-n"]).decode().strip()
    package_info = PackageInfo.from_poetry_version_output(poetry_version_output)

    print(f"Package name: {package_info.name}")
    print(f"Package version: {package_info.version}")

    if package_info.version == "0":
        print("No version to publish")
        return

    version_already_published = check_version_already_published(
        repo_json_api_url, package_info.name, package_info.version
    )
    if version_already_published:
        print(f"Version has already been published")
        return

    publish(repo_name)
    tag(package_info.version)


if __name__ == "__main__":
    main()
