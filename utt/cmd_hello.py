import datetime
from . import io

NAME = 'hello'

def add_args(parser):
    pass

def execute(args):
    io.add_entry(args.data_filename,
                 io.Entry(datetime.datetime.today(), 'hello'))
