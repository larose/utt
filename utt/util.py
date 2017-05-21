import errno
import os
import datetime

from .entry import Entry

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# PUBLIC
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def add_entry(filename, new_entry):
    _create_directories_for_file(filename)
    entries = list(entries_from_file(filename))
    new_day = False
    if entries:
        last_entry = entries[-1]
        new_day = new_entry.datetime.date() != last_entry.datetime.date()
    _append_line_to_file(filename, str(new_entry), insert_blank_line=new_day)


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
                    raise SyntaxError("Invalid syntax at line %d: %s" %
                                      (i, string))

                if previous_entry and \
                   previous_entry.datetime > new_entry.datetime:
                    raise Exception(
                        "Error line %d. Not in chronological order: %s > %s" %
                        (i, previous_entry, new_entry))
                previous_entry = new_entry
                yield new_entry
    except IOError:
        pass


def parse_datetime(datetimestring):
    return datetime.datetime.strptime(datetimestring, "%Y-%m-%d %H:%M")


def utt_touch_path(szPath):
    try:
        os.makedirs(szPath, 0o770)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

    return szPath


def user_data_dir():
    szPath = os.getenv('XDG_DATA_HOME', os.path.expanduser("~/.local/share"))
    szPath = os.path.join(szPath, 'utt')
    return utt_touch_path(szPath)


def utt_filename():
    return os.path.join(user_data_dir(), 'utt.log')


def utt_debug_log():
    return os.path.join(user_data_dir(), 'debug.log')


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# PRIVATE
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


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
