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

from pydidery.help import helping as h
from pydidery.diderying import ValidationError
from ioflo.aid import odict

try:
    import simplejson as json
except ImportError:
    import json


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
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True),
)
def main(upload, rotate, retrieve, data, consensus, v, config):
    verbose = v if v <= 4 else 4
    preloads = []

    if upload and rotate or upload and retrieve or rotate and retrieve:
        click.echo("Cannot combine --upload, --rotate, or --retrieve")
        return

    configData = h.parseConfigFile(config)

    try:
        if upload:
            preloads.extend(uploadSetup(upload, data, configData))

        if rotate:
            preloads.extend(rotateSetup(rotate, data, configData))

        if retrieve:
            preloads.extend(retrieveSetup(retrieve))

    except ValidationError as ex:
        return

    projectDirpath = os.path.dirname(
        os.path.dirname(
            os.path.abspath(
                os.path.expanduser(__file__)
            )
        )
    )
    floScriptpath = os.path.join(projectDirpath, "pydidery/flo/main.flo")

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


def uploadSetup(upload, dataFile, config):
    data = {}
    if dataFile is None:
        if upload == 'otp':
            click.echo('Data file required to upload otp blobs. Use --data, -d [file path]')
            raise ValidationError('Data file required to upload otp blobs. Use --data, -d [file path]')
        elif upload == 'history':
            history, sk = keyInception()

            config["current_sk"] = sk

            data = {
                "history": history
            }
    else:
        if "current_sk" not in config or config["current_sk"] == "":
            click.echo("Current signing key required to upload data.")
            raise ValidationError("Current signing key required to upload data.")

        data = h.parseDataFile(dataFile, upload)

    preloads = [
        ('.main.upload.servers', odict(value=config["servers"])),
        ('.main.upload.data', odict(value=data)),
        ('.main.upload.did', odict(value=config["did"])),
        ('.main.upload.sk', odict(value=config["current_sk"])),
    ]

    if "consensus" in config:
        preloads.append(('.main.upload.consensus', odict(value=config["consensus"])))

    return preloads


def rotateSetup(rotate, data, config):
    if rotate and data is None:
        click.echo('Data file required to start rotation event. Use --data, -d [file path]')
        raise ValidationError('Data file required to start rotation event. Use --data, -d [file path]')
    else:
        pass

    preloads = [
        ('.main.upload.servers', odict(value=config["servers"])),
        ('.main.upload.data', odict(value=data)),
        ('.main.upload.did', odict(value=config["did"])),
        ('.main.upload.sk', odict(value=config["current_sk"])),
    ]

    if "consensus" in config:
        preloads.append(('.main.upload.consensus', odict(value=config["consensus"])))
    if "rotation_sk" in config:
        preloads.append(('.main.upload.psk', odict(value=config["rotation_sk"])))

    return preloads


def retrieveSetup(retrieve, config, consensus=None):
    if consensus is None:
        if "consensus" not in config or config["consensus"] == "":
            click.echo('Consensus level must be specified either via the cli or the config file.')
            raise ValidationError('Consensus level must be specified either via the cli or the config file.')
        consensus = config["consensus"]

    preloads = [
        ('.main.upload.servers', odict(value=config["servers"])),
        ('.main.upload.did', odict(value=config["did"])),
        ('.main.upload.consensus', odict(value=consensus))
    ]

    return preloads


def keyInception():
    vk, sk = h.genKeys()
    pvk, psk = h.genKeys()
    history = {
        "id": h.makeDid(vk),
        "signer": 0,
        "signers": [
            vk,
            pvk
        ]
    }

    with open('/tmp/didery.keys.json', 'w') as keyFile:
        keyFile.write(json.dumps({"current_sk": sk, "current_vk": vk, "pre_rotated_sk": psk, "pre_rotated_vk": pvk}))

    click.confirm('Keys have been generated and stored in /tmp/didery.keys.json. '
                  'Make a copy and store them securely this file will be deleted after this prompt finishes.')

    os.remove('/tmp/didery.keys.json')

    click.echo('/tmp/didery.keys.json deleted.')

    return history, sk

