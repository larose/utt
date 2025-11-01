import errno
import os

from .data_filename import DataFilename
from .entries import Entries


class AddEntry:
    def __init__(self, data_filename: DataFilename, entries: Entries):
        self._data_filename = data_filename
        self._entries = entries

    def __call__(self, new_entry):
        _create_directories_for_file(self._data_filename)
        insert_new_line_before = _insert_new_line(self._entries, new_entry)
        _append_line_to_file(
            self._data_filename,
            str(new_entry),
            insert_new_line_before=insert_new_line_before,
        )


def _append_line_to_file(filename, line, insert_new_line_before):
    try:
        with open(filename, "rb+") as file:
            file.seek(-1, os.SEEK_END)
            last_char = file.read(1)
            prepend_new_line = last_char != b"\n"
    except OSError as os_err:
        if os_err.errno not in [errno.EINVAL, errno.ENOENT]:
            raise
        prepend_new_line = False

    with open(filename, "a") as file:
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
