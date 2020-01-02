from typing import Generator, List, Tuple

from ..data_structures.entry import Entry
from .entry_lines import EntryLines
from .entry_parser import EntryParser
from .timezone_config import TimezoneConfig


class Entries:
    def __init__(self, entry_lines: EntryLines,
                 timezone_config: TimezoneConfig, entry_parser: EntryParser):
        self._entry_lines = entry_lines
        self._timezone_config = timezone_config
        self._entry_parser = entry_parser

    def __call__(self) -> List[Entry]:
        entries: List[Entry] = list(
            _parse_log(self._entry_lines(), self._entry_parser))
        return entries


def _parse_log(lines: List[Tuple[int, str]],
               entry_parser: EntryParser) -> Generator[Entry, None, None]:
    previous_entry = None
    for line_number, line in lines:
        parsed_line = _parse_line(previous_entry, line_number, line.strip(),
                                  entry_parser)

        if parsed_line is not None:
            previous_entry, entry = parsed_line
            yield entry


def _parse_line(previous_entry: Entry, line_number: int, line: str,
                entry_parser: EntryParser):
    # Ignore empty lines
    if not line:
        return None

    new_entry = entry_parser.parse(line)
    if new_entry is None:
        raise SyntaxError("Invalid syntax at line %d: %s" %
                          (line_number, line))

    if previous_entry and \
       previous_entry.datetime > new_entry.datetime:
        raise Exception("Error line %d. Not in chronological order: %s > %s" %
                        (line_number, previous_entry, new_entry))
    previous_entry = new_entry
    return previous_entry, new_entry
