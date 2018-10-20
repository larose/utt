import errno
import os
from .entry import Entry


class LogRepo:
    def __init__(self, data_filename, timezone_config, entry_parser):
        self._data_filename = data_filename
        self._timezone_config = timezone_config
        self._entry_parser = entry_parser

    def append_entry(self, new_entry):
        _create_directories_for_file(self._data_filename)
        entries = list(self.entries())
        new_day = False

        if entries:
            last_entry = entries[-1]
            new_day = new_entry.datetime.date() != last_entry.datetime.date()

        _append_line_to_file(
            self._data_filename, str(new_entry), insert_blank_line=new_day)

    def entries(self):
        try:
            with open(self._data_filename) as text:
                previous_entry = None
                for i, string in enumerate((string.strip() for string in text),
                                           1):
                    # Ignore empty strings
                    if not string:
                        continue

                    new_entry = self._entry_parser.parse(string)
                    if new_entry is None:
                        raise SyntaxError(
                            "Invalid syntax at line %d: %s" % (i, string))

                    if previous_entry and \
                       previous_entry.datetime > new_entry.datetime:
                        raise Exception(
                            "Error line %d. Not in chronological order: %s > %s"
                            % (i, previous_entry, new_entry))
                    previous_entry = new_entry
                    yield new_entry
        except IOError:
            pass


def _append_line_to_file(filename, string, insert_blank_line):
    try:
        with open(filename, 'rb+') as file:
            file.seek(-1, os.SEEK_END)
            last_char = file.read(1)
            prepend_new_line = last_char != b"\n"
    except EnvironmentError as e:
        if e.errno != errno.ENOENT:
            raise
        prepend_new_line = False

    with open(filename, 'a') as file:
        if prepend_new_line:
            file.write("\n")
        if insert_blank_line:
            file.write("\n")
        file.write(string)
        file.write("\n")


def _create_directories_for_file(filename):
    try:
        os.makedirs(os.path.dirname(filename))
    except OSError as err:
        # If the exception is errno.EEXIST, we ignore it
        if err.errno != errno.EEXIST:
            raise
