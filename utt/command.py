import argparse
from dataclasses import dataclass
from typing import Callable


@dataclass
class Command:
    name: str
    description: str
    handler_class: Callable[..., Callable[[None], None]]
    add_args: Callable[[argparse.ArgumentParser], None]
