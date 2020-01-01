from utt.constants import HELLO_ENTRY_NAME
from utt.entry import Entry


class V1:
    HELLO_ENTRY_NAME = HELLO_ENTRY_NAME
    Entry = Entry

    def __init__(self):
        self._commands = []

    def add_command(self, command_class):
        self._commands.append(command_class)
