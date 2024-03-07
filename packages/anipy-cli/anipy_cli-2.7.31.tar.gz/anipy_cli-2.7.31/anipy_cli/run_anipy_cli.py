#!/bin/python
from anipy_cli import cli
from anipy_cli.misc import keyboard_inter


def main():
    try:
        cli.run_cli()
    except KeyboardInterrupt:
        keyboard_inter()


if __name__ == "__main__":
    main()
