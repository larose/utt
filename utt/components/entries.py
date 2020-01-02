class Entries:
    def __init__(self, entry_lines, timezone_config, entry_parser):
        self._entry_lines = entry_lines
        self._timezone_config = timezone_config
        self._entry_parser = entry_parser

    def __call__(self):
        return list(_parse_log(self._entry_lines(), self._entry_parser))


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
