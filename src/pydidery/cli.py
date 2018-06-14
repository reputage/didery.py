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


"""
Command line interface for didery.py library.  Path to config file containing server list required
"""
@click.command()
@click.option(
    '--upload',
    multiple=False,
    type=click.Choice(['otp', 'history']),
    help="Choose the type of upload 'otp' or 'history'."
)
@click.option(
    '--rotate',
    multiple=False,
    is_flag=True,
    default=False,
    help='Send rotation event to didery servers.'
)
@click.option(
    '--retrieve',
    multiple=False,
    type=click.Choice(['otp', 'history']),
    help="Retrieve 'otp' or 'history' data."
)
@click.option(
    '--data',
    '-d',
    multiple=False,
    default=None,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True),
    help='Specify path to data file.'
)
@click.option(
    '--consensus',
    '-c',
    multiple=False,
    default=50,
    type=click.IntRange(0, 100),
    help='Threshold(%) at which consensus is reached.'
)
@click.option(
    '-v',
    multiple=False,
    count=True,
    help="Verbosity of console output. There are 5 verbosity levels from '' to '-vvvv.'"
)
@click.argument(
    'config',
    type=click.File('rw'),
)
def main(upload, rotate, retrieve, data, consensus, v, config):
    verbose = v if v <= 4 else 4

    if upload == 'otp' and data is None:
        click.echo('data file required to upload otp blobs. Use --data, -d [file path]')
        return

    if rotate and data is None:
        click.echo('data file required to start rotation event. Use --data, -d [file path]')
        return

    projectDirpath = os.path.dirname(
        os.path.dirname(
            os.path.abspath(
                os.path.expanduser(__file__)
            )
        )
    )
    floScriptpath = os.path.join(projectDirpath, "pydidery/flo/main.flo")

    with open(config) as conf:
        data = json.load(conf)
        print(data)

    """ Main entry point for ioserve CLI"""
    ioflo.app.run.run(  name="didery.py",
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
