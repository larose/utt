import errno
import os
from .entry import Entry

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# PUBLIC
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def add_entry(filename, entry):
    _create_directories_for_file(filename)
    _append_line_to_file(filename, str(entry))

def write_entries(filename, entries):
    _create_directories_for_file(filename)
    _write_lines_to_file(filename, (str(entry) for entry in entries))

def entries_from_file(filename):
    try:
        with open(filename) as text:
            previous_entry = None
            for i, string in enumerate((string.strip() for string in text), 1):
                # Ignore empty strings
                if not string:
                    continue

                new_entry = Entry.from_string(string)
                if new_entry is None:
                    raise SyntaxError(
                        "Invalid syntax at line %d: %s" % (i, string))

                if previous_entry and \
                   previous_entry.datetime > new_entry.datetime:
                    raise Exception(
                        "Error line %d. Not in chronological order: %s > %s" %
                        (i, previous_entry, new_entry))
                previous_entry = new_entry
                yield new_entry
    except IOError:
        pass


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# PRIVATE
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def _append_line_to_file(filename, string):
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
        file.write(string)
        file.write("\n")

def _write_lines_to_file(filename, strings):
    with open(filename, 'w') as file:
        for string in strings:
            file.write(string)
            file.write("\n")

def _create_directories_for_file(filename):
    try:
        os.makedirs(os.path.dirname(filename))
    except OSError as err:
        # If the exception is errno.EEXIST, we ignore it
        if err.errno != errno.EEXIST:
            raise
