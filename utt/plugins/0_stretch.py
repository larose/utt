import argparse
import copy

from ..api import _v1
from ..components.add_entry import AddEntry  # Private API
from ..components.timezone_config import TimezoneConfig  # Private API


class StretchHandler:
    def __init__(
        self,
        args: argparse.Namespace,
        now: _v1.Now,
        add_entry: AddEntry,
        entries: _v1.Entries,
        timezone_config: TimezoneConfig,
        output: _v1.Output,
    ):
        self._args = args
        self._now = now
        self._add_entry = add_entry
        self._entries = entries
        self._timezone_config = timezone_config
        self._output = output

    def __call__(self):
        if not self._entries:
            raise Exception("No entry to stretch")
        latest_entry = self._entries[-1]
        new_entry = _v1.Entry(self._now, latest_entry.name, False, comment=latest_entry.comment)
        self._add_entry(new_entry)
        print("stretched " + str(_localize(self._timezone_config, latest_entry)), file=self._output)
        print("        → " + str(_localize(self._timezone_config, new_entry)), file=self._output)


def _localize(timezone_config, new_entry):
    if timezone_config.enabled():
        return new_entry

    new_entry = copy.deepcopy(new_entry)
    new_entry.datetime = new_entry.datetime.replace(tzinfo=None)
    return new_entry


stretch_command = _v1.Command(
    name="stretch",
    description="Stretch the latest task to the current time",
    handler_class=StretchHandler,
    add_args=lambda p: None,
)


_v1.register_command(stretch_command)
