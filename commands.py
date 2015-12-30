from docopt import docopt


class AbstractCommand:
    """Base class for the commands"""

    def __init__(self, command_args, global_args):
        """
        Initialize the commands.

        :param command_args: arguments of the command
        :param global_args: arguments of the program
        """
        self.args = docopt(self.__doc__, argv=command_args)
        self.global_args = global_args

    def execute(self):
        """Execute the commands"""
        raise NotImplementedError


class Run(AbstractCommand):
    """
    Defines how long a player will run.

    usage:
        run ( --distance=<meters> | --time=<seconds> )

    options:
        --distance=<meters>     Player runs for <meters> meters.
        --time=<seconds>        Player run for <seconds> seconds.
    """

    def execute(self):
        if self.args['--distance']:
            if int(self.args['--distance']) > 100:
                print('Are you crazy? {} is not going to do that!'.format(self.global_args['--name']))
                return
            print('{} is going to run {} meters.'.format(self.global_args['--name'], self.args['--distance']))
        elif self.args['--time']:
            if int(self.args['--time']) > 10:
                print('Are you crazy? {} not going to do that!'.format(self.global_args['--name']))
                return
            print('{} is going to run for {} seconds.'.format(self.global_args['--name'], self.args['--time']))


class Jump(AbstractCommand):
    """
    Defines how far a player will jump.

    usage:
        jump --distance=<meters>

    options:
        --distance=<meters>     Player jumps for <meters> meters.
    """

    def execute(self):
        print('{} is going to jump {} meters.'.format(self.global_args['--name'], self.args['--distance']))

class Greet(AbstractCommand):
    """
    Greets others players.

    usage:
        greet
    """

    def execute(self):
        print('Hi other player(s)!')
