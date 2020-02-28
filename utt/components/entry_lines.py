from typing import List, Tuple

from .data_filename import DataFilename


class EntryLines:
    def __init__(self, data_filename: DataFilename):
        self._data_filename = data_filename

    def __call__(self) -> List[Tuple[int, str]]:
        try:
            return self._get_lines()
        except IOError:
            return []

    def _get_lines(self) -> List[Tuple[int, str]]:
        with open(self._data_filename) as entry_file:
            return list(enumerate(entry_file, 1))
