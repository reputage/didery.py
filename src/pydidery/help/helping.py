from ..diderying import ValidationError

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


def parseJson(data, requireds=()):
    """
        Returns deserialized version of data string if data is correctly formed.
        Otherwise returns None

        :param data is json encoded unicode string
        :param requireds tuple of string keys required in json data
        """

    try:
        # now validate message data
        try:
            dat = json.loads(data, object_pairs_hook=ODict)
        except ValueError as ex:
            raise ValidationError("Invalid JSON")  # invalid json

        if not dat:  # registration must not be empty
            raise ValidationError("Empty body")

        if not isinstance(dat, dict):  # must be dict subclass
            raise ValidationError("JSON not dict")

        for field in requireds:
            if field not in dat:
                raise ValidationError("Missing required field {}".format(field))

    except ValidationError:
        raise

    except Exception as ex:  # unknown problem
        raise ValidationError("Unexpected error")

    return dat


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
