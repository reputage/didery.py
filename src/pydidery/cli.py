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

from pydidery.help import helping as h
from pydidery.diderying import ValidationError
from pydidery.lib import generating as gen

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
    '-v',
    multiple=False,
    count=True,
    help="Verbosity of console output. There are 5 verbosity levels from '' to '-vvvv.'"
)
@click.argument(
    'config',
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True),
)
def main(upload, rotate, retrieve, v, config):
    verbose = v if v <= 4 else 4
    preloads = [
        ('.main.upload.verbosity', odict(value=verbose)),
        ('.main.retrieve.verbosity', odict(value=verbose)),
        ('.main.rotate.verbosity', odict(value=verbose)),
        ('.main.upload.start', odict(value=True if upload else False)),
        ('.main.retrieve.start', odict(value=True if retrieve else False)),
        ('.main.rotate.start', odict(value=True if rotate else False))
    ]

    if upload and rotate or upload and retrieve or rotate and retrieve:
        click.echo("Cannot combine --upload, --rotate, or --retrieve")
        return

    configData = h.parseConfigFile(config)

    try:
        if upload:
            preloads.extend(uploadSetup(upload, configData))

        if rotate:
            preloads.extend(rotateSetup(rotate, configData))

        if retrieve:
            preloads.extend(retrieveSetup(retrieve, configData))

    except ValidationError as ex:
        click.echo(str(ex))
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
                        verbose=0,
                        consolepath='',
                        statistics=False,
                        preloads=preloads)


def uploadSetup(upload, config):
    data = {}
    sk = None

    if upload == "otp":
        path = click.prompt(
            "Please enter a path to the data file: ",
            type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True)
        )

        data = h.parseDataFile(path, upload)

        sk = click.prompt("Please enter you signing/private key: ")

    if upload == "history":
        if click.confirm("Would you like to generate key pairs?"):
            history, sk = historyInit()
            data = history
        else:
            path = click.prompt(
                "Please enter a path to the data file: ",
                type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True)
            )

            data = h.parseDataFile(path, upload)

            sk = click.prompt("Please enter you signing/private key: ")


    preloads = [
        ('.main.upload.servers', odict(value=config["servers"])),
        ('.main.upload.data', odict(value=data)),
        ('.main.upload.sk', odict(value=sk)),
        ('.main.upload.type', odict(value=upload)),
    ]

    return preloads


def rotateSetup(rotate, config):
    if click.confirm("Do you have a data file?"):
        path = click.prompt(
            "Please enter a path to the data file: ",
            type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True)
        )

        data = h.parseDataFile(path, "history")
    else:
        # TODO: Query didery servers for current data using did in config
        data = {"signers": []}

    csk = click.prompt("Please enter your current signing/private key: ")
    rsk = click.prompt("Please enter the signing/private key you are rotating to: ")

    if click.confirm("Do you need a new pre-rotated key pair generated"):
        pvk, psk = keyery()
        data["signers"].append(pvk)
        data["signer"] = int(data["signer"]) + 1

    preloads = [
        ('.main.rotate.servers', odict(value=config["servers"])),
        ('.main.rotate.data', odict(value=data)),
        ('.main.rotate.did', odict(value=config["did"])),
        ('.main.rotate.sk', odict(value=csk)),
        ('.main.rotate.psk', odict(value=rsk))
    ]

    return preloads


def retrieveSetup(retrieve, config):
    preloads = [
        ('.main.retrieve.servers', odict(value=config["servers"])),
        ('.main.retrieve.did', odict(value=config["did"])),
        ('.main.retrieve.type', odict(value=retrieve))
    ]

    return preloads


def historyInit():
    history, vk, sk, pvk, psk = gen.historyGen()

    with open('/tmp/didery.keys.json', 'w') as keyFile:
        keys = {
            "current_sk": sk,
            "current_vk": vk,
            "pre_rotated_sk": psk,
            "pre_rotated_vk": pvk
        }

        keyFile.write(json.dumps(keys, encoding='utf-8'))

    click.prompt('\nKeys have been generated and stored in /tmp/didery.keys.json. \n\n'
                 'Make a copy and store them securely. \n'
                 'The file will be deleted after you enter a key')

    os.remove('/tmp/didery.keys.json')

    click.echo('/tmp/didery.keys.json deleted.')

    return history, sk


def keyery():
    sk, vk = gen.keyGen()

    with open('/tmp/didery.keys.json', 'w') as keyFile:
        keys = {
            "signing_key": sk,
            "verification_key": vk
        }

        keyFile.write(json.dumps(keys, encoding='utf-8'))

    click.prompt('\nKeys have been generated and stored in /tmp/didery.keys.json. \n\n'
                 'Make a copy and store them securely. \n'
                 'The file will be deleted after you enter a key')

    os.remove('/tmp/didery.keys.json')

    click.echo('/tmp/didery.keys.json deleted.')

    return vk, sk
