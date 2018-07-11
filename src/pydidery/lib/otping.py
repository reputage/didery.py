import arrow

try:
    import simplejson as json
except ImportError:
    import json

from ..help import helping as h
from ..help import consensing
from ..lib import generating as gen


def patronHelper(method="GET", path="blob", headers=None, data=None):
    result = yield from h.httpRequest(method, path=path, headers=headers, data=data)

    return result['body'].decode(), result['status']


# def getAllOtpBlobs(urls=None):
#     if urls is None:
#         urls = ["http://localhost:8080/history", "http://localhost:8000/history"]
#
#     generators = []
#
#     for url in urls:
#         generators.append(patronHelper(path=url))
#
#     return h.awaitAsync(generators)


def getOtpBlob(did, urls=None):
    if urls is None:
        urls = ["http://localhost:8080", "http://localhost:8000"]

    generators = {}

    for url in urls:
        endpoint = "{0}/{1}/{2}".format(url, "blob", did)
        generators[url] = patronHelper(path=endpoint)

    data = h.awaitAsync(generators)

    return consensing.consense(data, "otp")


def postOtpBlob(data, sk, urls=None):
    if urls is None:
        urls = ["http://localhost:8080", "http://localhost:8000"]

    generators = {}
    data['changed'] = str(arrow.utcnow())
    bdata = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode()
    headers = {
        "Signature": 'signer="{0}"'.format(gen.signResource(bdata, gen.key64uToKey(sk)))
    }

    for url in urls:
        endpoint = "{0}/{1}".format(url, "blob")
        generators[url] = patronHelper(method="POST", path=endpoint, data=data, headers=headers)

    return h.awaitAsync(generators)


def putOtpBlob(did, data, sk, urls=None):
    if urls is None:
        urls = ["http://localhost:8080", "http://localhost:8000"]

    generators = {}
    data['changed'] = str(arrow.utcnow())
    bdata = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode()
    headers = {
        "Signature": 'signer="{0}"'.format(gen.signResource(bdata, gen.key64uToKey(sk)))
    }

    for url in urls:
        endpoint = "{0}/{1}/{2}".format(url, "blob", did)
        generators[url] = patronHelper(method="PUT", path=endpoint, data=data, headers=headers)

    return h.awaitAsync(generators)
