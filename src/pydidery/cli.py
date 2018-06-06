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


"""
Command line interface for didery.py library.  Path to config file containing server list required
"""
@click.command()
@click.argument(
    'config',
    type=click.File(),
)
@click.option(
    '--save',
    multiple=False,
    type=click.Choice(['create-otp', 'update-otp', 'create-history', 'update-history']),
    help='choose the type of save'
)
@click.option(
    '--retrieve',
    multiple=False,
    type=click.Choice(['otp', 'history']),
    help='retrieve otp or history data'
)
@click.option(
    '--data',
    '-d',
    multiple=False,
    default=[None, None],
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True),
    help='path to data file'
)
@click.option(
    '--consensus',
    '-c',
    multiple=False,
    default=50,
    type=click.IntRange(0, 100),
    help='threshold(%) at which consensus is reached'
)
@click.option(
    '-v',
    multiple=False,
    count=True,
    help='verbosity of console output'
)
def main(config, save, retrieve, data, consensus, verbose):
    projectDirpath = os.path.dirname(
        os.path.dirname(
            os.path.abspath(
                os.path.expanduser(__file__)
            )
        )
    )
    floScriptpath = os.path.join(projectDirpath, "pydidery/flo/main.flo")

    """ Main entry point for ioserve CLI"""
    click.echo(verbose)
    # verbose = verbose-1
    if verbose < 4:
        verbose = 4

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
