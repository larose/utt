# pylint: disable=protected-access
import importlib
import pkgutil
import sys

import utt.plugins
from utt.api import _v1  # pylint: disable=protected-access


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
        sys.argv.append('--help')

    load_plugins()
    getattr(_v1._container, f"commands/{_v1._container.args.command}")()  # pylint: disable=protected-access, no-member


if __name__ == '__main__':
    main()
