# -*- coding: utf-8 -*-
from . import util
from .entry import Entry

NAME = 'stretch'

def add_args(parser):
    pass

def execute(args):
    entries = list(util.entries_from_file(args.data_filename))
    if len(entries) == 0:
        raise Exception("No entry to stretch")
    old_entry = Entry(
            entries[-1].datetime,
            entries[-1].name,
            entries[-1].is_current_entry)
    entries[-1].datetime = args.now
    util.write_entries(args.data_filename, entries)
    print("stretched " + str(old_entry))
    print("        → " + str(entries[-1]))
