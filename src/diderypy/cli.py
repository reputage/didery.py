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

from diderypy.help import helping as h
from diderypy.diderying import ValidationError
from diderypy.lib import generating as gen

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
    '-i',
    multiple=False,
    is_flag=True,
    default=False,
    help="Send a key rotation history inception event."
)
@click.option(
    '--upload',
    '-u',
    is_flag=True,
    default=False,
    help="Upload a new otp encrypted private key."
)
@click.option(
    '--rotate',
    '-r',
    multiple=False,
    is_flag=True,
    default=False,
    help='Rotate public/private key pairs.'
)
@click.option(
    '--update',
    '-U',
    multiple=False,
    is_flag=True,
    default=False,
    help='Update otp encrypted private key.'
)
@click.option(
    '--retrieve',
    '-R',
    multiple=False,
    is_flag=True,
    default=False,
    help="Retrieve key rotation history."
)
@click.option(
    '--download',
    '-d',
    multiple=False,
    is_flag=True,
    default=False,
    help="Download otp encrypted private key."
)
@click.option(
    '--delete',
    '-D',
    multiple=False,
    is_flag=True,
    default=False,
    help="Delete rotation history."
)
@click.option(
    '--remove',
    '-m',
    multiple=False,
    is_flag=True,
    default=False,
    help="Remove otp encrypted private key."
)
@click.option(
    '--events',
    '-e',
    multiple=False,
    is_flag=True,
    default=False,
    help="Pull a record of all history rotation events for a specified did."
)
@click.option(
    '-v',
    multiple=False,
    count=True,
    help="Verbosity of console output. There are 5 verbosity levels from '' to '-vvvv.'"
)
@click.option(
    '--mute',
    '-M',
    multiple=False,
    is_flag=True,
    default=False,
    help="Mute all console output except prompts."
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
@click.option(
    '--save',
    multiple=False,
    type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True, readable=True, resolve_path=True),
    help="Directory to store generated key files in."
)
@click.option(
    '--keys',
    multiple=True,
    default=None,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True),
    help="File(s) where keys are stored in a json format"
)
@click.argument(
    'config',
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True),
)
def main(incept, upload, rotate, update, retrieve, download, delete, remove, events, v, mute, data, did, save, keys, config):
    if mute:
        verbose = 0
    else:
        v = 1 if v == 0 else v

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
        ('.main.events.verbosity', odict(value=verbose)),
        ('.main.incept.start', odict(value=True if incept else False)),
        ('.main.upload.start', odict(value=True if upload else False)),
        ('.main.rotate.start', odict(value=True if rotate else False)),
        ('.main.update.start', odict(value=True if update else False)),
        ('.main.retrieve.start', odict(value=True if retrieve else False)),
        ('.main.download.start', odict(value=True if download else False)),
        ('.main.delete.start', odict(value=True if delete else False)),
        ('.main.remove.start', odict(value=True if remove else False)),
        ('.main.events.start', odict(value=True if events else False))
    ]

    options = [incept, upload, rotate, update, retrieve, download, delete, remove, events]
    count = options.count(True)
    if count > 1:
        click.echo("Cannot combine --incept --upload, --rotate, --update, --retrieve, --download, --delete, --remove, or --events.")
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
            preloads.extend(inceptSetup(configData, data, save, keys))

        if upload:
            preloads.extend(uploadSetup(configData, data, keys))

        if rotate:
            preloads.extend(rotateSetup(configData, data, save, keys))

        if update:
            preloads.extend(updateSetup(configData, data, keys))

        if retrieve:
            preloads.extend(retrieveSetup(configData, did))

        if download:
            preloads.extend(downloadSetup(configData, did))

        if delete:
            preloads.extend(deleteSetup(configData, did, keys))

        if remove:
            preloads.extend(removeSetup(configData, did, keys))

        if events:
            preloads.extend(eventsSetup(configData, did))

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
    floScriptpath = os.path.join(projectDirpath, "diderypy/flo/main.flo")

    """ Main entry point for ioserve CLI"""
    ioflo.app.run.run(  name="didery.py",
                        period=0.125,
                        real=True,
                        retro=True,
                        filepath=floScriptpath,
                        behaviors=['diderypy.core'],
                        mode='',
                        username='',
                        password='',
                        verbose=0,
                        consolepath='',
                        statistics=False,
                        preloads=preloads)


def inceptSetup(config, data, path, key_paths):

    if data is None:
        if key_paths:
            click.echo("\nWARN: Key file will not be used unless a data file is provided with --data.\n")
        history, sk = historyInit(path)
        data = history
    else:
        data = h.parseDataFile(data, "history")

        keys = getSigningKeys(key_paths)
        sk = keys[0]

    preloads = [
        ('.main.incept.servers', odict(value=config["servers"])),
        ('.main.incept.data', odict(value=data)),
        ('.main.incept.sk', odict(value=sk))
    ]

    return preloads


def uploadSetup(config, data, key_paths):
    if data is None:
        raise ValueError("Data file required. Use --data=path/to/file")

    data = h.parseDataFile(data, "otp")

    keys = getSigningKeys(key_paths)
    sk = keys[0]

    preloads = [
        ('.main.upload.servers', odict(value=config["servers"])),
        ('.main.upload.data', odict(value=data)),
        ('.main.upload.sk', odict(value=sk))
    ]

    return preloads


def rotateSetup(config, data, path, key_paths):
    if data is None:
        raise ValueError("Data file required. Use --data=path/to/file")

    data = h.parseDataFile(data, "history")

    keys = getSigningKeys(key_paths, 2)

    if click.confirm("Generate a new pre-rotated key pair?"):
        pvk, psk = keyery(path)
        data["signers"].append(pvk)
        data["signer"] = int(data["signer"]) + 1

    preloads = [
        ('.main.rotate.servers', odict(value=config["servers"])),
        ('.main.rotate.data', odict(value=data)),
        ('.main.rotate.did', odict(value=data["id"])),
        ('.main.rotate.sk', odict(value=keys[0])),
        ('.main.rotate.psk', odict(value=keys[1]))
    ]

    return preloads


def updateSetup(config, data, key_paths):
    if data is None:
        raise ValueError("Data file required. Use --data=path/to/file")

    data = h.parseDataFile(data, "otp")

    keys = getSigningKeys(key_paths)
    sk = keys[0]

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


def deleteSetup(config, did, key_paths):
    if did is None:
        raise ValueError("did required. Use --did")

    h.validateDid(did)

    keys = getSigningKeys(key_paths)
    sk = keys[0]

    preloads = [
        ('.main.delete.servers', odict(value=config["servers"])),
        ('.main.delete.did', odict(value=did)),
        ('.main.delete.sk', odict(value=sk))
    ]

    return preloads


def removeSetup(config, did, key_paths):
    if did is None:
        raise ValueError("did required. Use --did")

    h.validateDid(did)

    keys = getSigningKeys(key_paths)
    sk = keys[0]

    preloads = [
        ('.main.remove.servers', odict(value=config["servers"])),
        ('.main.remove.did', odict(value=did)),
        ('.main.remove.sk', odict(value=sk))
    ]

    return preloads


def eventsSetup(config, did):
    if did is None:
        raise ValueError("did required. Use --did")

    h.validateDid(did)

    preloads = [
        ('.main.events.servers', odict(value=config["servers"])),
        ('.main.events.did', odict(value=did))
    ]

    return preloads


def historyInit(directory):
    didBoxInit = gen.DidBox()
    didBoxRot = gen.DidBox()
    history, vk, sk, pvk, psk = gen.historyGen(didBoxInit.seed, didBoxRot.seed)

    if directory is None:
        init_path = "./didery_keys_initial.json"
        rot_path = "./didery_keys_rotation.json"
    else:
        init_path = os.path.join(directory, "didery_keys_initial.json")
        rot_path = os.path.join(directory, "didery_keys_rotation.json")
        click.echo('Saving initial key pair to {}'.format(init_path))
        click.echo('Saving pre-rotated key pair to {}'.format(rot_path))

    didBoxInit.save64(init_path)
    didBoxRot.save64(rot_path)

    if directory is None:
        try:
            click.prompt('\nKeys generated in: '
                         ''
                         '\n\n./didery_keys_initial.json\n'
                         './didery_keys_rotation.json\n\n'
                         ''
                         'Make a copy and store them securely. \n'
                         'The file will be deleted after pressing any key+Enter')

            os.remove("./didery_keys_initial.json")
            os.remove("./didery_keys_rotation.json")

            click.echo('Key files deleted.')
        except KeyboardInterrupt as ex:
            if os.path.exists("./didery_keys_initial.json"):
                os.remove("./didery_keys_initial.json")
            if os.path.exists("./didery_keys_rotation.json"):
                os.remove("./didery_keys_rotation.json")

            click.echo('Key files deleted.')
            raise

    return history, sk


def keyery(directory):
    didBox = gen.DidBox()

    if directory is None:
        path = "./didery_prerotated_key.json"
    else:
        path = os.path.join(directory, "didery_prerotated_key.json")
        click.echo('Saving new key pair to {}'.format(path))

    didBox.save64(path)

    if directory is None:
        try:
            click.prompt('\nKeys generated in: '
                         ''
                         '\n\n./didery_prerotated_key.json\n\n'
                         ''
                         'Make a copy and store them securely. \n'
                         'The file will be deleted after pressing any key+Enter')

            os.remove('didery_prerotated_key.json')

            click.echo('Key files deleted.')
        except KeyboardInterrupt as ex:
            if os.path.exists("./didery_prerotated_key.json"):
                os.remove("./didery_prerotated_key.json")
                click.echo('Key file deleted.')
            raise

    return didBox.base64_vk(), didBox.base64_sk()


def getSigningKeys(path=None, keys_to_obtain=1):
    csk = None
    psk = None

    if not path:
        csk = click.prompt("Enter your current signing/private key")

        if keys_to_obtain > 1:
            psk = click.prompt("Enter your pre-rotated signing/private key")
    else:
        keys = gen.DidBox()
        keys.open(path[0])
        csk = keys.base64_sk()

        if keys_to_obtain > 1:
            keys = gen.DidBox()
            keys.open(path[1])
            psk = keys.base64_sk()

    return [csk, psk]
