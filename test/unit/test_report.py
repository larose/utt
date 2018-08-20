import os
import unittest

try:
    import unittest.mock as mock
except ImportError:
    import mock

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

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
    stdout : str
        Content from the mocked stdout.
    stderr : str
        Content from the mocked stderr.
    exception : SystemExit or None
        If no error occurs, None is returned.
    """
    mocked_argv = mock.patch("sys.argv", ["utt"] + argv)
    stdout = StringIO()
    stderr = StringIO()
    mocked_stdout = mock.patch("sys.stdout", stdout)
    mocked_stderr = mock.patch("sys.stderr", stderr)
    try:
        with mocked_stdout, mocked_stderr, mocked_argv:
            main()
    except SystemExit as exc:
        exception = exc
    else:
        exception = None
    return stdout.getvalue(), stderr.getvalue(), exception


class TestReport(unittest.TestCase):
    def test_report_range(self):
        argv = [
            "--data",
            DATA_FILENAME,
            "--now",
            "2014-3-19 18:30",
            "report",
            "--from",
            "2014-03-15",
            "--to",
            "2014-03-19",
            "--no-current-activity",
        ]
        stdout, stderr, exception = call_command(argv)

        with open(os.path.join(DATA_DIR, "utt-range.stdout"), "r") as f:
            expected_content = f.read()
        self.assertIsNone(exception, stderr)
        self.assertEqual(stdout, expected_content)

    def test_report_wednesday(self):
        argv = [
            "--data",
            DATA_FILENAME,
            "--now",
            "2014-3-19 18:30",
            "report",
            "wednesday",
        ]
        stdout, stderr, exception = call_command(argv)
        with open(os.path.join(DATA_DIR, "utt-1.stdout"), "r") as f:
            expected_content = f.read()
        self.assertIsNone(exception, stderr)
        self.assertEqual(stdout, expected_content)

    def test_report_overnight_activity_ignored(self):
        data_filename = os.path.join(DATA_DIR, "utt-overnight.log")
        argv = [
            "--data",
            data_filename,
            "--now",
            "2014-3-19 18:30",
            "report",
            "2014-03-14",
        ]

        stdout, stderr, exception = call_command(argv)
        with open(os.path.join(DATA_DIR, "utt-overnight.stdout"), "r") as f:
            expected_content = f.read()
        self.assertIsNone(exception, stderr)
        self.assertEqual(stdout, expected_content)

    def test_report_single_day_in_the_past(self):
        data_filename = os.path.join(DATA_DIR, "utt-upper-case.log")
        argv = [
            "--data",
            data_filename,
            "--now",
            "2014-3-19 18:30",
            "report",
            "2014-03-14",
        ]

        stdout, stderr, exception = call_command(argv)
        with open(os.path.join(DATA_DIR, "utt-upper-case.stdout"), "r") as f:
            expected_content = f.read()

        self.assertIsNone(exception, stderr)
        first_line, rest = stdout.split("\n", 1)

        # This ignored activity comes from current activity
        self.assertEqual(
            first_line,
            "WARN: Ignored 1 overnight activity, total time: 5 days, 8:00:00")

        self.assertEqual(rest, expected_content)
