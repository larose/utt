import errno
import copy
import os

from .log_parser import parse_log


class LogRepo:
    def __init__(self, data_filename, timezone_config, entry_parser,
                 local_timezone):
        self._data_filename = data_filename
        self._timezone_config = timezone_config
        self._entry_parser = entry_parser
        self._local_timezone = local_timezone

    def append_entry(self, new_entry):
        _create_directories_for_file(self._data_filename)
        entries = self.entries()
        insert_new_line_before = _insert_new_line(entries, new_entry)
        new_entry = _localize(self._timezone_config, self._local_timezone,
                              new_entry)
        _append_line_to_file(
            self._data_filename,
            str(new_entry),
            insert_new_line_before=insert_new_line_before)

    def entries(self):
        try:
            return self._parse_file()
        except IOError:
            pass

    def _parse_file(self):
        with open(self._data_filename) as log_file:
            lines = list(enumerate(log_file, 1))

        return list(parse_log(lines, self._entry_parser))


def _append_line_to_file(filename, line, insert_new_line_before):
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
        if insert_new_line_before:
            file.write("\n")
        file.write(line)
        file.write("\n")


def _create_directories_for_file(filename):
    try:
        os.makedirs(os.path.dirname(filename))
    except OSError as err:
        # If the exception is errno.EEXIST, we ignore it
        if err.errno != errno.EEXIST:
            raise


def _insert_new_line(entries, new_entry):
    if not entries:
        return False

    last_entry = entries[-1]
    return last_entry.datetime.date() != new_entry.datetime.date()


def _localize(timezone_config, local_timezone, new_entry):
    if not timezone_config.enabled():
        return new_entry

    new_entry = copy.deepcopy(new_entry)
    new_entry.datetime = local_timezone.localize(new_entry.datetime)
    return new_entry
