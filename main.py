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

import commands

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0.0', options_first=True)

    # Retrieve the command to execute.
    command_name = args.pop('<command>').capitalize()

    # Retrieve the command arguments.
    command_args = args.pop('<args>')
    if command_args is None:
        command_args = {}

    # After 'poping' '<command>' and '<args>', what is left in the args dictionary are the global arguments.

    # Retrieve the class from the 'commands' module.
    try:
        command_class = getattr(commands, command_name)
    except AttributeError:
        print('Unknown command. RTFM!.')
        raise DocoptExit()
        exit(1)

    # Create an instance of the command.
    command = command_class(command_args, args)

    # Execute the command.
    command.execute()
