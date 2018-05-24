"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -m py-dideryd` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``py-didery.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``py-didery.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import os
import click
import ioflo.app.run

from ioflo.aid import odict
from ioflo.aid.consoling import VERBIAGE_NAMES


@click.command()
@click.option(
    '--Consensus',
    '-C',
    multiple=False,
    default=50,
    type=click.IntRange(0, 100),
    help='threshold(%) at which consensus is reached'
)
@click.option(
    '--config',
    '-c',
    multiple=False,
    nargs=1,
    help='specify config file path'
)
@click.option(
    '--data',
    '-d',
    multiple=False,
    nargs=1,
    help='specify data file path'
)
@click.option(
    '--verbose',
    '-v',
    multiple=False,
    type=click.Choice(VERBIAGE_NAMES),
    default=VERBIAGE_NAMES[0],
    help='console output verbosity level'
)
def main(consensus, config, data, verbose):
    projectDirpath = os.path.dirname(
        os.path.dirname(
            os.path.abspath(
                os.path.expanduser(__file__)
            )
        )
    )
    floScriptpath = os.path.join(projectDirpath, "pydidery/flo/main.flo")

    """ Main entry point for ioserve CLI"""

    verbose = VERBIAGE_NAMES.index(verbose)

    ioflo.app.run.run(  name="skedder",
                        period=0.125,
                        real=True,
                        retro=True,
                        filepath=floScriptpath,
                        behaviors=['pydidery.core'],
                        mode='',
                        username='',
                        password='',
                        verbose=verbose,
                        consolepath='',
                        statistics=False,
                        preloads=[('.main.server.port', odict(value=""))])
