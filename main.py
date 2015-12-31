#! /usr/bin/env python
"""
Control center for an imaginary video game.

usage:
    control [-hv] [-n NAME] <command> [<args>]

options:
    -h, --help                  shows the help
    -n NAME --name=NAME         sets player name [default: player]
    -v, --version               shows the version

The subcommands are:
    greet   greets other players
    jump    makes the player jump
    run     makes the player run
"""

from docopt import docopt
from docopt import DocoptExit

from commands import Greet
from commands import Jump
from commands import Run

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0.0', options_first=True)

    # Retrieve the command to execute.
    command_name = args.pop('<command>').lower()

    # Retrieve the command arguments.
    command_args = args.pop('<args>')
    if command_args is None:
        command_args = {}

    # After 'poping' '<command>' and '<args>', what is left in the args dictionary are the global arguments.
    if command_name == 'greet':
        command = Greet(command_args, args)
    elif command_name == 'jump':
        command = Jump(command_args, args)
    elif command_name == 'run':
        command = Run(command_args, args)
    else:
        print('Unknown command. RTFM!.')
        raise DocoptExit()
        exit(1)

    command.execute()
