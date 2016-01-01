DocOpt Subcommands Example
==========================

This is a simple example to explain the usage of subcommands with `DocOpt`_. For a more basic usage of `DocOpt`_ please refer to the official website.

The example
-----------

This example depicts a imaginary video game where we control a player, and we can make him/her jump, run and greet other players.

Usage example
^^^^^^^^^^^^^

To start this tutorial, here are some usage examples and their outputs.

The ``greet`` subcommand:

.. code-block:: bash

    $ python main.py greet
    Hi other player(s)!

The ``run`` subcommand:

.. code-block:: bash

    $ python main.py run --distance=10
    player is going to run 10 meters.

The ``run`` subcommand with a ``name`` for our player:

.. code-block:: bash

    $ python main.py -n Rémy run --distance=10000
    Are you crazy? Rémy is not going to do that!

Using a command which has not been created (yet):

.. code-block:: bash

    $ python main.py -n Rémy shoot
    Unknown command. RTFM!.
    usage:
        control [-hv] [-n NAME] <command> [<args>]


main.py
^^^^^^^

The main command is defined in the ``main.py`` module. Its help screen looks like this:

.. code-block:: python

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

This help screen comes directly from the docstring of the program, define in ``main.py``, line 2-15.

We can see that the program has 3 optional arguments:

    * help, which displays the help screen
    * name, which sets the player name
    * version, which shows the version number

And also expects a command (``<command>``) with optional arguments (``[<args>]``).

``DocOpt`` is going to parse the command line for you, but we will have to use it in a certain way to ensure the arguments are passed correctly to the subcommands:

.. code-block:: python

    25 args = docopt(__doc__, version='1.0.0', options_first=True)

In this line, we tell ``DocOpt`` to generate the CLI by reading the main docstring of the program (``__doc__``), we set the version of the program to ``1.0.0``, and we enable the subcommands with ``options_first=True``. The result is stored in a dictionary named ``args``.

Now that our ``args`` dictionary is populated, we can extract the name of the subcommand to execute:

.. code-block:: python

    28 command_name = args.pop('<command>').capitalize()

As well as its arguments:

.. code-block:: python

    31 command_args = args.pop('<args>')

.. note::

    If there is no argument for a command, ``command_args`` must be set to an empty dictionary (``DocOpt`` sets it to ``None`` otherwise).


    .. code-block:: python

        32 if command_args is None:
        33     command_args = {}

Now our ``args`` dictionary contains only the global arguments. They will be made available to **ALL** the subcommands.

For this example, it is assumed that a player must have a name, therefore the ``NAME`` argument was made global.

Find the command to execute
"""""""""""""""""""""""""""

`DocOpt`_ does not provide a dispatcher to find the right function to execute, so we have to route the commands ourselves.

The first option is to use a bunch of ``if ... elif ... else``:

.. code-block:: python

    if command_name == 'Greet':
        command = Greet(command_args, args)
    elif command_name == 'Jump':
        command = Jump(command_args, args)
    elif command_name == 'Run':
        command = Run(command_args, args)
    else:
        print('Unknown command. RTFM!.')
        raise DocoptExit()
        exit(1)

But that is not a very clean solution.

A more elegant approach is to leverage the `getattr`_ function from the python library:

.. code-block:: python

    try:
        command_class = getattr(commands, command_name)
    except AttributeError:
        print('Unknown command. RTFM!.')
        raise DocoptExit()
        exit(1)

commands.py
^^^^^^^^^^^

The ``commands.py`` module contains all our subcommands.

We organized them by providing a ``AbstractCommand`` class which will be used as the base class of all our subcommands.

This class uses ``DocOpt`` to parse the command arguments:

.. code-block:: python

    14 self.args = docopt(self.__doc__, argv=command_args)

Stores the global arguments provided by the main module:

.. code-block:: python

    15 self.global_args = global_args

And also defines all the functions that are expected in each subcommand:

.. code-block:: python

    17 def execute(self):
    18     """Execute the commands"""
    19     raise NotImplementedError

Then each subcommand will be created by subclassing ``AbstractCommand``:

.. code-block:: python

    22 class Run(AbstractCommand):

    ...

    47 class Jump(AbstractCommand):

The class docstring will define the usage, the arguments and the options of the subcommand. Each subcommand will be responsible of defining its own behavior.

Each subcommand will reimplement the ``execute`` function, which will define the actions of the subcommand. For example, the ``execute`` function of the ``greet`` subcommands looks like this:

.. code-block:: python

    def execute(self):
        print('Hi other player(s)!')

.. _`DocOpt`: http://docopt.org/
.. _`getattr`: https://docs.python.org/2/library/functions.html?highlight=getattr#getattr
