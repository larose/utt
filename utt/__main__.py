import importlib
import pkgutil
import sys

import utt.plugins
from utt.container import create_container


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
    container = create_container()

    # pylint: disable=no-member
    getattr(container, 'command/{}'.format(container.args.command))()


if __name__ == '__main__':
    main()
