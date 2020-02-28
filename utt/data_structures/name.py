import re


class Name:
    NAME_REGEX = re.compile(r"(?P<project>[^\s:]+):\s(?P<task>.*)")

    def __init__(self, name: str):
        self.name = name
        match = Name.NAME_REGEX.match(name)
        if match is None:
            self.task = name
            self.project = ""
            return

        groupdict = match.groupdict()
        self.project = groupdict["project"]
        self.task = groupdict["task"]

    def __lt__(self, other):
        return self.name < other.name

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Name(" + ", ".join([self.name, self.task, self.project]) + ")"
