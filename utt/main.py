import argparse
import importlib
import pkgutil
import sys

import utt.plugins
from utt.api import _v1
from utt.components.commands import Commands


def iter_namespace(ns_pkg):
    # Specifying the second argument (prefix) to iter_modules makes the
    # returned name an absolute name instead of a relative one. This allows
    # import_module to work without having to do additional modification to
    # the name.
    #
    # Source: https://packaging.python.org/guides/creating-and-discovering-plugins/
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")


def load_plugins():
    for _, name, _ in iter_namespace(utt.plugins):
        importlib.import_module(name)


def main():
    if len(sys.argv) == 1:
        sys.argv.append("--help")

    load_plugins()

    command_name = _v1._private.container[argparse.Namespace].command

    commands: Commands = _v1._private.container[Commands]
    for command in commands:
        if command.name == command_name:
            _v1._private.container[command.handler_class]()
