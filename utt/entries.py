class Entries:
    def __init__(self, data_filename, timezone_config, entry_parser,
                 local_timezone):
        self._data_filename = data_filename
        self._timezone_config = timezone_config
        self._entry_parser = entry_parser
        self._local_timezone = local_timezone

    def __call__(self):
        try:
            return self._parse_file()
        except IOError:
            return []

    def _parse_file(self):
        with open(self._data_filename) as log_file:
            lines = list(enumerate(log_file, 1))

        return list(_parse_log(lines, self._entry_parser))


def _parse_log(lines, entry_parser):
    previous_entry = None
    for line_number, line in lines:
        parsed_line = _parse_line(previous_entry, line_number, line.strip(),
                                  entry_parser)

        if parsed_line is not None:
            previous_entry, entry = parsed_line
            yield entry


def _parse_line(previous_entry, line_number, line, entry_parser):
    # Ignore empty lines
    if not line:
        return None

    new_entry = entry_parser.parse(line)
    if new_entry is None:
        raise SyntaxError(
            "Invalid syntax at line %d: %s" % (line_number, line))

    if previous_entry and \
       previous_entry.datetime > new_entry.datetime:
        raise Exception("Error line %d. Not in chronological order: %s > %s" %
                        (line_number, previous_entry, new_entry))
    previous_entry = new_entry
    return previous_entry, new_entry
