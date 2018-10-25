import sys

from .container import container


def main():
    if len(sys.argv) == 1:
        sys.argv.append('--help')

    getattr(container, 'command/{}'.format(container.args.command))()


if __name__ == '__main__':
    main()
