import datetime
import re
from typing import Optional

from ..data_structures.entry import Entry

DATE_REGEX = r"(?P<date>\d{4}-\d{1,2}-\d{1,2}\s+\d{1,2}:\d{1,2})"
NAME_REGEX = r"\s+(?P<name>[^\s].*?)"
COMMENT_REGEX = r"\s{2}#\s(?P<comment>.*$)?"

ENTRY_REGEX = re.compile("".join([DATE_REGEX, NAME_REGEX, r"($|", COMMENT_REGEX, ")"]))


class EntryParser:
    def parse(self, string: str) -> Optional[Entry]:
        match = ENTRY_REGEX.match(string)

        if match is None:
            return None

        groupdict = match.groupdict()

        if "date" not in groupdict or "name" not in groupdict:
            return None

        date_str = groupdict["date"]
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M")

        name = groupdict["name"]
        comment = groupdict.get("comment")
        return Entry(date, name, False, comment=comment)
