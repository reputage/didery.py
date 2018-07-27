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
    '--incept',
    multiple=False,
    is_flag=True,
    default=False,
    help="Send a key rotation history inception event."
)
@click.option(
    '--upload',
    is_flag=True,
    default=False,
    help="Upload a new otp encrypted private key."
)
@click.option(
    '--rotate',
    multiple=False,
    is_flag=True,
    default=False,
    help='Rotate public/private key pairs.'
)
@click.option(
    '--update',
    multiple=False,
    is_flag=True,
    default=False,
    help='Update otp encrypted private key.'
)
@click.option(
    '--retrieve',
    multiple=False,
    is_flag=True,
    default=False,
    help="Retrieve key rotation history."
)
@click.option(
    '--download',
    multiple=False,
    is_flag=True,
    default=False,
    help="Download otp encrypted private key."
)
@click.option(
    '--delete',
    multiple=False,
    is_flag=True,
    default=False,
    help="Delete rotation history."
)
@click.option(
    '--remove',
    multiple=False,
    is_flag=True,
    default=False,
    help="Remove otp encrypted private key."
)
@click.option(
    '-v',
    multiple=False,
    count=True,
    help="Verbosity of console output. There are 5 verbosity levels from '' to '-vvvv.'"
)
@click.option(
    '--data',
    multiple=False,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True),
    help="Path to the data file."
)
@click.option(
    '--did',
    multiple=False,
    help="decentralized identifier(did)."
)
@click.argument(
    'config',
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True),
)
def main(incept, upload, rotate, update, retrieve, download, delete, remove, v, data, did, config):
    verbose = v if v <= 4 else 4
    preloads = [
        ('.main.incept.verbosity', odict(value=verbose)),
        ('.main.upload.verbosity', odict(value=verbose)),
        ('.main.rotate.verbosity', odict(value=verbose)),
        ('.main.update.verbosity', odict(value=verbose)),
        ('.main.retrieve.verbosity', odict(value=verbose)),
        ('.main.download.verbosity', odict(value=verbose)),
        ('.main.delete.verbosity', odict(value=verbose)),
        ('.main.remove.verbosity', odict(value=verbose)),
        ('.main.incept.start', odict(value=True if incept else False)),
        ('.main.upload.start', odict(value=True if upload else False)),
        ('.main.rotate.start', odict(value=True if rotate else False)),
        ('.main.update.start', odict(value=True if update else False)),
        ('.main.retrieve.start', odict(value=True if retrieve else False)),
        ('.main.download.start', odict(value=True if download else False)),
        ('.main.delete.start', odict(value=True if delete else False)),
        ('.main.remove.start', odict(value=True if remove else False))
    ]

    options = [incept, upload, rotate, update, retrieve, download, delete, remove]
    count = options.count(True)
    if count > 1:
        click.echo("Cannot combine --incept --upload, --rotate, --update, --retrieve, or --download")
        return
    if count == 0:
        click.echo("No options given. For help use --help. Exiting Didery.py")
        return

    try:
        configData = h.parseConfigFile(config)
    except ValidationError as err:
        click.echo("Error parsing the config file: {}.".format(err))
        return

    try:
        if incept:
            preloads.extend(inceptSetup(configData, data))

        if upload:
            preloads.extend(uploadSetup(configData, data))

        if rotate:
            preloads.extend(rotateSetup(configData, data))

        if update:
            preloads.extend(updateSetup(configData, data))

        if retrieve:
            preloads.extend(retrieveSetup(configData, did))

        if download:
            preloads.extend(downloadSetup(configData, did))

        if delete:
            preloads.extend(deleteSetup(configData, did))

        if remove:
            preloads.extend(removeSetup(configData, did))

    except (ValidationError, ValueError) as ex:
        click.echo("Error setting up didery.py: {}.".format(ex))
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


def inceptSetup(config, data):
    if data is None:
        history, sk = historyInit()
        data = history
    else:
        data = h.parseDataFile(data, "history")

        sk = click.prompt("Please enter you signing/private key")

    preloads = [
        ('.main.incept.servers', odict(value=config["servers"])),
        ('.main.incept.data', odict(value=data)),
        ('.main.incept.sk', odict(value=sk))
    ]

    return preloads


def uploadSetup(config, data):
    if data is None:
        raise ValueError("Data file required. Use --data=path/to/file")

    data = h.parseDataFile(data, "otp")

    sk = click.prompt("Please enter you signing/private key")

    preloads = [
        ('.main.upload.servers', odict(value=config["servers"])),
        ('.main.upload.data', odict(value=data)),
        ('.main.upload.sk', odict(value=sk))
    ]

    return preloads


def rotateSetup(config, data):
    if data is None:
        raise ValueError("Data file required. Use --data=path/to/file")

    data = h.parseDataFile(data, "history")

    csk = click.prompt("Please enter your current signing/private key")
    rsk = click.prompt("Please enter the signing/private key you are rotating to")

    if click.confirm("Do you need a new pre-rotated key pair generated"):
        pvk, psk = keyery()
        data["signers"].append(pvk)
        data["signer"] = int(data["signer"]) + 1

    preloads = [
        ('.main.rotate.servers', odict(value=config["servers"])),
        ('.main.rotate.data', odict(value=data)),
        ('.main.rotate.did', odict(value=data["id"])),
        ('.main.rotate.sk', odict(value=csk)),
        ('.main.rotate.psk', odict(value=rsk))
    ]

    return preloads


def updateSetup(config, data):
    if data is None:
        raise ValueError("Data file required. Use --data=path/to/file")

    data = h.parseDataFile(data, "otp")

    sk = click.prompt("Please enter you signing/private key")

    preloads = [
        ('.main.update.servers', odict(value=config["servers"])),
        ('.main.update.data', odict(value=data)),
        ('.main.update.did', odict(value=data["id"])),
        ('.main.update.sk', odict(value=sk))
    ]

    return preloads


def retrieveSetup(config, did):
    if did is None:
        raise ValueError("did required. Use --did")

    h.validateDid(did)

    preloads = [
        ('.main.retrieve.servers', odict(value=config["servers"])),
        ('.main.retrieve.did', odict(value=did))
    ]

    return preloads


def downloadSetup(config, did):
    if did is None:
        raise ValueError("did required. Use --did")

    h.validateDid(did)

    preloads = [
        ('.main.download.servers', odict(value=config["servers"])),
        ('.main.download.did', odict(value=did))
    ]

    return preloads


def deleteSetup(config, did):
    if did is None:
        raise ValueError("did required. Use --did")

    h.validateDid(did)

    sk = click.prompt("Please enter your signing/private key")

    preloads = [
        ('.main.delete.servers', odict(value=config["servers"])),
        ('.main.delete.did', odict(value=did)),
        ('.main.delete.sk', odict(value=sk))
    ]

    return preloads


def removeSetup(config, did):
    if did is None:
        raise ValueError("did required. Use --did")

    h.validateDid(did)

    sk = click.prompt("Please enter your signing/private key")

    preloads = [
        ('.main.remove.servers', odict(value=config["servers"])),
        ('.main.remove.did', odict(value=did)),
        ('.main.remove.sk', odict(value=sk))
    ]

    return preloads


def historyInit():
    history, vk, sk, pvk, psk = gen.historyGen()

    with open('didery.keys.json', 'w') as keyFile:
        keys = {
            "current_sk": sk,
            "current_vk": vk,
            "pre_rotated_sk": psk,
            "pre_rotated_vk": pvk
        }

        keyFile.write(json.dumps(keys, encoding='utf-8'))

    click.prompt('\nKeys have been generated and stored in the current directory under didery.keys.json. \n\n'
                 'Make a copy and store them securely. \n'
                 'The file will be deleted after you enter a key')

    os.remove('didery.keys.json')

    click.echo('didery.keys.json deleted.')

    return history, sk


def keyery():
    sk, vk = gen.keyGen()

    with open('didery.keys.json', 'w') as keyFile:
        keys = {
            "signing_key": sk,
            "verification_key": vk
        }

        keyFile.write(json.dumps(keys, encoding='utf-8'))

    click.prompt('\nKeys have been generated and stored in the current directory under didery.keys.json. \n\n'
                 'Make a copy and store them securely. \n'
                 'The file will be deleted after you enter a key')

    os.remove('didery.keys.json')

    click.echo('didery.keys.json deleted.')

    return vk, sk
