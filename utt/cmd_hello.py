from . import util
from .entry import Entry

NAME = 'hello'

def add_args(parser):
    pass

def execute(args):
    util.add_entry(args.data_filename,
                   Entry(args.now, 'hello', False))
