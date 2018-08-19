import contextlib
import os
import sys
import unittest

try:
    import unittest.mock as mock
except ImportError:
    import mock

try:
    from io import StringIO
except ImportError:
    from cStringIO import StringIO

from utt.__main__ import main

DATA_DIR = os.path.join(os.path.dirname(__file__), "../integration/data")
DATA_FILENAME = os.path.join(DATA_DIR, "utt-1.log")


def call_command(argv):
    """ Mock stdout and sys.argv in order to call command.
    Return the stdout content and SystemExit encountered (if any)

    Parameters
    ----------
    argv: list of str
        List of command line arguments, excluding utt itself.

    Returns
    -------
    content : str
        Content from the mocked stdout.
    exception : SystemExit or None
        If no error occurs, None is returned.
    """
    mocked_argv = mock.patch("sys.argv", ["utt"] + argv)
    stdout = StringIO()
    mocked_stdout = mock.patch("sys.stdout", stdout)
    try:
        with mocked_stdout, mocked_argv:
            main()
    except SystemExit as exc:
        exception = exc
    else:
        exception = None
    content = stdout.getvalue()
    return content, exception


class TestReport(unittest.TestCase):

    def test_report_range(self):
        argv = [
            "report",
            "--data", DATA_FILENAME,
            "--from", "2014-03-14",
            "--to", "2014-03-19",
        ]
        content, exception = call_command(argv)
        self.assertIsNone(exception)
        self.assertEqual(content, "")

    def test_report_wednesday(self):
        argv = [
            "--data", DATA_FILENAME,
            "--now", "2014-3-19 18:30",
            "report",
            "wednesday",
        ]
        content, exception = call_command(argv)

        with open(os.path.join(DATA_DIR, "utt-1.stdout"), "r") as f:
            expected_content = f.read()

        self.assertIsNone(exception)
        self.assertEqual(content, expected_content)
