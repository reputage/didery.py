import arrow

try:
    import simplejson as json
except ImportError:
    import json

from urllib.parse import urlparse

from ..help import helping as h
from ..lib import generating as gen


def patronHelper(method="GET", scheme=u'', host="localhost", port=None, path="blob", headers=None, data=None, body=b''):
    result = yield from h.httpRequest(method,
                                      scheme=scheme,
                                      host=host,
                                      port=port,
                                      path=path,
                                      headers=headers,
                                      data=data,
                                      body=body)

    return result['body'].decode(), result['status']


def getAllOtpBlobs(url="http://localhost:8080"):
    pass


def getOtpBlob(did, url="http://localhost:8080"):
    pass


def postOtpBlob(data, sk, url="http://localhost:8080"):
    pass


def putOtpBlob(did, data, sk, psk, url="http://localhost:8080"):
    pass
