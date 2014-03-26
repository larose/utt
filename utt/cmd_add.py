import datetime
from . import util
from .entry import Entry

NAME = 'add'

def add_args(parser):
    parser.add_argument("name")

def execute(args):
    util.add_entry(args.data_filename,
                   Entry(datetime.datetime.today(), args.name, False))
