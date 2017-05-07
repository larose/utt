from . import util
from .entry import Entry

import os
import logging

NAME = 'add'
DESCRIPTION = 'Add a completed task'


def ACDB_Search(pathDB, szPrefix):

    setItems = set()

    # LOAD TIME-STRIPPED, TRIMMED, VALUES INTO SET FOR UNIQUENESS
    with open(pathDB, "r") as fDB:

        for line in fDB:

            szItem = line.strip()

            if(len(szItem) > 17):

                szItem = szItem[17:]

                if(szItem.startswith(szPrefix)):
                    setItems.add(szItem)

        fDB.close()

    return sorted(setItems)


def ACDB_Completer(**kwargs):

    try:

        pathDB = util.utt_filename()

        # RETURN LIST OF TASKS THAT MATCH PREFIX
        if(os.path.exists(pathDB)):
            return ACDB_Search(pathDB, kwargs['prefix'])

        return []

    except Exception as e:

        logging.debug("ACDB_Completer", exc_info=True)

    return ["ERROR:_SEE_%s_FOR_DETAILS" % (util.utt_debug_log())]



def add_args(parser):
    parser.add_argument(
        "name", help="completed task description").completer = ACDB_Completer



def execute(args):
    util.add_entry(args.data_filename, Entry(args.now, args.name, False))
