import subprocess
import sys


def main():
    version_filename = sys.argv[1]

    version = subprocess.check_output(["poetry", "version"], stderr=sys.stderr).decode().split()[1]

    print(f"Writing '{version}' to {version_filename}")
    with open(version_filename, "w") as version_txt:
        version_txt.write(version)


if __name__ == "__main__":
    main()
