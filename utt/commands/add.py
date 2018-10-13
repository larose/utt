from .. import util
from ..entry import Entry

import os
import logging


class AddCommand:
    NAME = 'add'
    DESCRIPTION = 'Add a completed task'

    def add_args(self, parser):
        parser.add_argument(
            "name",
            help="completed task description").completer = acbd_completer

    def __call__(self, args):
        util.add_entry(args.data_filename, Entry(args.now, args.name, False))


Command = AddCommand


def acdb_search(path_db, prefix):

    setItems = set()

    # Load time-stripped, trimmed, values into set for uniqueness
    with open(path_db, "r") as db:
        for line in db:
            szItem = line.strip()
            if len(szItem) > 17:
                szItem = szItem[17:]
                if szItem.startswith(prefix):
                    setItems.add(szItem)

    return sorted(setItems)


def acbd_completer(**kwargs):
    try:
        path_db = util.utt_filename()

        # Return list of tasks that match prefix
        if os.path.exists(path_db):
            return acdb_search(path_db, kwargs['prefix'])

        return []

    except Exception as e:
        logging.debug("acbd_completer", exc_info=True)

    return ["ERROR:_SEE_%s_FOR_DETAILS" % (util.utt_debug_log())]
