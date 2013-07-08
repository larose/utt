import datetime
from . import io

NAME = 'add'

def add_args(parser):
    parser.add_argument("name")

def execute(args):
    io.add_entry(args.data_filename,
                 io.Entry(datetime.datetime.today(), args.name))
