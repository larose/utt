class EntryLines:
    def __init__(self, data_filename):
        self._data_filename = data_filename

    def __call__(self):
        try:
            return self._get_lines()
        except IOError:
            return []

    def _get_lines(self):
        with open(self._data_filename) as entry_file:
            lines = list(enumerate(entry_file, 1))
        return lines
