from . import util
from .entry import Entry

NAME = 'hello'
DESCRIPTION = 'Say \'hello\' when you arrive in the morning...'


def add_args(parser):
    pass


def execute(args):
    util.add_entry(args.data_filename, Entry(args.now, 'hello', False))
