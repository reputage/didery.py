import arrow

try:
    import simplejson as json
except ImportError:
    import json

from ..help import helping as h
from ..help import consensing
from ..help import signing as sign
from ..lib import generating as gen


def __patronHelper(method="GET", path="history", headers=None, data=None):
    result = yield from h.httpRequest(method, path=path, headers=headers, data=data)

    if result:
        return result['body'].decode(), result.get('status')
    else:
        return None


# def getAllHistories(urls=None):
#     if urls is None:
#         urls = ["http://localhost:8080/history", "http://localhost:8000/history"]
#
#     generators = []
#
#     for url in urls:
#         generators.append(__patronHelper(path=url))
#
#     return h.awaitAsync(generators)


def getHistory(did, urls):
    consense = consensing.Consense()
    if not urls:
        raise ValueError("At least one url required.")

    generators = {}

    for url in urls:
        endpoint = "{0}/{1}/{2}".format(url, "history", did)
        generators[endpoint] = __patronHelper(path=endpoint)

    data = h.awaitAsync(generators)

    return consense.consense(data)


def postHistory(data, sk, urls):
    if not urls:
        raise ValueError("At least one url required.")

    if not sk:
        raise ValueError("Signing key required.")

    generators = {}
    data['changed'] = str(arrow.utcnow())
    bdata = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode()
    headers = {
        "Signature": 'signer="{0}"'.format(sign.signResource(bdata, gen.key64uToKey(sk)))
    }

    for url in urls:
        endpoint = "{0}/{1}".format(url, "history")
        generators[endpoint] = __patronHelper(method="POST", path=endpoint, data=data, headers=headers)

    return h.awaitAsync(generators)


def putHistory(data, sk, psk, urls):
    if not urls:
        raise ValueError("At least one url required.")

    if not sk:
        raise ValueError("Signing key required.")

    if not psk:
        raise ValueError("Pre-rotated signing key required.")

    generators = {}
    did = data["id"]
    data['changed'] = str(arrow.utcnow())
    bdata = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode()
    headers = {
        "Signature": 'signer="{0}"; rotation="{1}"'.format(
            sign.signResource(bdata, gen.key64uToKey(sk)),
            sign.signResource(bdata, gen.key64uToKey(psk))
        )
    }

    for url in urls:
        endpoint = "{0}/{1}/{2}".format(url, "history", did)
        generators[endpoint] = __patronHelper(method="PUT", path=endpoint, data=data, headers=headers)

    return h.awaitAsync(generators)


def deleteHistory(did, sk, urls):
    if not urls:
        raise ValueError("At least one url required.")

    if not sk:
        raise ValueError("Signing key required.")

    generators = {}
    data = {"id": did}
    bdata = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode()
    headers = {
        "Signature": 'signer="{0}"'.format(
            sign.signResource(bdata, gen.key64uToKey(sk))
        )
    }

    for url in urls:
        endpoint = "{0}/{1}/{2}".format(url, "history", did)
        generators[endpoint] = __patronHelper(method="DELETE", path=endpoint, data=data, headers=headers)

    return h.awaitAsync(generators)
