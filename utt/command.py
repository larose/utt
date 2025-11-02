import argparse
import typing
from dataclasses import dataclass
from typing import Callable


@dataclass
class Command:
    name: str
    description: str
    handler_class: typing.Type
    add_args: Callable[[argparse.ArgumentParser], None]
