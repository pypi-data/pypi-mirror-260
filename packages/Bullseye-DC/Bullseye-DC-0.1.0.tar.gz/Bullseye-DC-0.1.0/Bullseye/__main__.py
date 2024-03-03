from .config import get_config
from .Bullseye import DiscordCli, __version__
import os.path
import readline
import sys

USAGE = """\
Usage:
  Bullseye.py [--debug]
  Bullseye.py -h | --help | --version
"""


def main():
    args = sys.argv[1:]
    if "-h" in args or "--help" in args:
        print(USAGE, end="")
        return

    if "--version" in args:
        print(__version__)
        return

    debug = True
    try:
        args.pop(args.index("--debug"))
    except ValueError:
        debug = False

    if args:
        print(USAGE, file=sys.stderr, end="")
        sys.exit(1)

    cli = DiscordCli(debug=debug)
    readline.set_auto_history(True)
    history_path = os.path.join(os.path.expanduser("~"), ".Bullseye_history")

    try:
        readline.read_history_file(history_path)
    except FileNotFoundError:
        pass

    try:
        cli.command_loop()
    finally:
        readline.write_history_file(history_path)
        get_config().save()


if __name__ == "__main__":
    main()
