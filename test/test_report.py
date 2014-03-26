import collections
import datetime
import ddt
import os
import unittest
from io import StringIO
from unittest import mock

import utt.cmd_report

REAL_PATH_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
DATA_DIRECTORY = os.path.join(REAL_PATH_DIRECTORY, 'data')
VALID_ENTRIES = [
    {
        'args': {
            "report_date": datetime.date(2014, 3, 19),
            "data_filename": 'utt-1.log',
            "current_activity": "-- Current Activity --",
            "no_current_activity": False,
            "now": datetime.datetime(2014, 3, 19, 18, 30)
        },
        'expected_output_filename': 'utt-1.stdout'
    }
]

Args = collections.namedtuple('Args',
                              ['report_date', 'data_filename',
                               'current_activity', 'no_current_activity',
                               'now'])

@ddt.ddt
class Report(unittest.TestCase):
    maxDiff = None

    @ddt.data(*VALID_ENTRIES)
    @ddt.unpack
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_output_with_valid_entries(self, stdout_mock, args,
                                       expected_output_filename):
        args['data_filename'] = os.path.join(DATA_DIRECTORY,
                                             args['data_filename'])
        args = Args(**args)
        with open(os.path.join(DATA_DIRECTORY, expected_output_filename)) as f:
            expected_output = f.read()
        utt.cmd_report.execute(args)
        self.assertEqual(expected_output, stdout_mock.getvalue())
