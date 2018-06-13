import base64
import libnacl

from ..diderying import ValidationError

from collections import OrderedDict as ODict
from copy import deepcopy
try:
    import simplejson as json
except ImportError:
    import json

from ioflo.aid import odict
from ioflo.aio.http import Patron
from ioflo.aio import WireLog
from ioflo.base import Store
from ioflo.aid import timing
from ioflo.aid import getConsole
console = getConsole()


def genKeys():
    seed = libnacl.randombytes(libnacl.crypto_sign_SEEDBYTES)
    vk, sk = libnacl.crypto_sign_seed_keypair(seed)

    return vk, sk


def makeDid(vk, method="dad"):
    """
    Create and return Indigo Did from bytes vk.
    vk is 32 byte verifier key from EdDSA (Ed25519) keypair
    """
    # convert verkey to jsonable unicode string of base64 url-file safe
    vk64u = base64.urlsafe_b64encode(vk).decode("utf-8")
    did = "did:{}:{}".format(method, vk64u)
    return did


def extractDidSignerParts(signer, method="dad"):
    """
    Parses and returns did index keystr from signer key indexed did
    as tuple (did, index, keystr)
    raises ValueError if fails parsing
    """
    # get signer key from read data. assumes that resource is valid
    try:
        did, index = signer.rsplit("#", maxsplit=1)
        index = int(index)  # get index and sdid from signer field
    except ValueError as ex:
        raise ValueError("Invalid indexed signer value")

    try:  # correct did format  pre:method:keystr
        pre, meth, keystr = did.split(":")
    except ValueError as ex:
        raise ValueError("Malformed DID value")

    if pre != "did" or meth != method:
        raise ValueError("Invalid DID value")

    return (did, index, keystr)


def parseJsonFile(file, requireds=()):
    """
        Returns deserialized version of data string if data is correctly formed.
        Otherwise returns None

        :param file is json encoded unicode string
        :param requireds tuple of string keys required in json data
        """
    data = None

    with open(file) as f:
        try:
            # now validate message data
            try:
                data = json.load(f, object_pairs_hook=ODict)
            except ValueError as ex:
                raise ValidationError("Invalid JSON")  # invalid json

            if not data:  # registration must not be empty
                raise ValidationError("Empty body")

            if not isinstance(data, dict):  # must be dict subclass
                raise ValidationError("JSON not dict")

            for field in requireds:
                if field not in data:
                    raise ValidationError("Missing required field {}".format(field))

        except ValidationError:
            raise

        except Exception as ex:  # unknown problem
            print(ex)
            raise ValidationError("Unexpected error")

    return data


def secureConfigFile(file, data):
    secureData = deepcopy(data)
    secureData['current_sk'] = ""
    secureData['rotation_sk'] = ""

    with open(file, 'w') as f:
        f.write(json.dumps(secureData, encoding='utf-8'))


def parseConfigFile(file):
    """
    Validate the data in the configuration file
    :param file: click.Path object
    :param upload: upload otp blob or rotation history
    :param rotate: rotation event
    :return: parsed configuration data
    """
    data = parseJsonFile(file, ["servers", "did"])

    # Check for valid did
    extractDidSignerParts(data["did"])

    if not isinstance(data["servers"], list):
        raise ValidationError('"servers" field must be a list.')

    return data


def parseDataFile(file, dtype):
    data = {}

    if dtype == "history":
        data = parseJsonFile(file, ["history"])

        for field in ["id", "signer", "signers"]:
            if field not in data["history"]:
                raise ValidationError("Missing required field {}".format(field))

    if dtype == "otp":
        data = parseJsonFile(file, ["otp"])

        for field in ["id", "blob"]:
            if field not in data["otp"]:
                raise ValidationError("Missing required field {}".format(field))

    # Check for valid did
    extractDidSignerParts(data[dtype]["id"])

    return data


def backendRequest(method=u'GET',
                   scheme=u'',  #default if not in path
                   host=u'localhost',  # default if not in path
                   port=None, # default if not in path
                   path=u'/',
                   qargs=None,
                   data=None,
                   store=None,
                   timeout=2.0,
                   buffer=False,
                   ):
    """
    Perform Async ReST request to Backend Server

    Parameters:

    Usage: (Inside a generator function)

        response = yield from backendRequest()

    response is the response if valid else None
    before response is completed the yield from yields up an empty string ''
    once completed then response has a value

    path can be full url with host port etc  path takes precedence over others


    """
    store = store if store is not None else Store(stamp=0.0)
    if buffer:
        wlog = WireLog(buffify=buffer, same=True)
        wlog.reopen()
    else:
        wlog = None

    headers = odict([('Accept', 'application/json'),
                     ('Connection', 'close')])

    client = Patron(bufsize=131072,
                    wlog=wlog,
                    store=store,
                    scheme=scheme,
                    hostname=host,
                    port=port,
                    method=method,
                    path=path,
                    qargs=qargs,
                    headers=headers,
                    data=data,
                    reconnectable=False,
                    )

    console.concise("Making Backend Request {0} {1} ...\n".format(method, path))

    client.transmit()
    # assumes store clock is advanced elsewhere
    timer = timing.StoreTimer(store=store, duration=timeout)
    while ((client.requests or client.connector.txes or not client.responses)
           and not timer.expired):
        try:
            client.serviceAll()
        except Exception as ex:
            console.terse("Error: Servicing backend client. '{0}'\n".format(ex))
            raise ex
        yield b''  # this is eventually yielded by wsgi app while waiting

    response = None  # in case timed out
    if client.responses:
        response = client.responses.popleft()
    client.close()
    if wlog:
        wlog.close()

    return response
