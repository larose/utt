import sys

from .container import create_container


def main():
    if len(sys.argv) == 1:
        sys.argv.append('--help')

    container = create_container()

    # pylint: disable=no-member
    getattr(container, 'command/{}'.format(container.args.command))()


if __name__ == '__main__':
    main()
