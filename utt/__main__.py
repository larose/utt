import sys

from .container import CONTAINER


def main():
    if len(sys.argv) == 1:
        sys.argv.append('--help')

    # pylint: disable=no-member
    getattr(CONTAINER, 'command/{}'.format(CONTAINER.args.command))()


if __name__ == '__main__':
    main()
