import arrow

try:
    import simplejson as json
except ImportError:
    import json

from urllib.parse import urlparse

from ..help import helping as h
from ..lib import generating as gen


def patronHelper(method="GET", scheme=u'', host="localhost", port=None, path="history", headers=None, data=None, body=b''):
    result = yield from h.httpRequest(method, scheme=scheme, host=host, port=port, path=path, headers=headers, data=data, body=body)

    return result['body'].decode(), result['status']


def getAllHistories(url="http://localhost:8080"):
    url_parts = urlparse(url)

    response = patronHelper(scheme=url_parts.scheme, host=url_parts.netloc)

    while True:
        try:
            next(response)
        except StopIteration as si:
            return si.value


def getDidHistory(did, url="http://localhost:8080"):
    url_parts = urlparse(url)
    path = "{0}/{1}".format("history", did)

    response = patronHelper(scheme=url_parts.scheme, host=url_parts.netloc, path=path)

    while True:
        try:
            next(response)
        except StopIteration as si:
            return si.value


def postHistory(data, sk, url="http://localhost:8080"):
    url_parts = urlparse(url)

    data['changed'] = str(arrow.utcnow())

    bdata = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode()

    headers = {
        "Signature": 'signer="{0}"'.format(gen.signResource(bdata, gen.key64uToKey(sk)))
    }

    response = patronHelper(method="POST", scheme=url_parts.scheme, host=url_parts.netloc, data=data, headers=headers)

    while True:
        try:
            next(response)
        except StopIteration as si:
            return si.value


def putHistory(did, data, sk, psk, url="http://localhost:8080"):
    url_parts = urlparse(url)
    path = "{0}/{1}".format("history", did)

    data['changed'] = str(arrow.utcnow())

    bdata = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode()

    headers = {
        "Signature": 'signer="{0}"; rotation="{1}"'.format(
            gen.signResource(bdata, gen.key64uToKey(sk)),
            gen.signResource(bdata, gen.key64uToKey(psk))
        )
    }

    response = patronHelper(method="PUT", scheme=url_parts.scheme, host=url_parts.netloc, path=path, data=data, headers=headers)

    while True:
        try:
            next(response)
        except StopIteration as si:
            return si.value


def getAllHistoriesAsync(url="http://localhost:8080"):
    url_parts = urlparse(url)

    response = yield from patronHelper(scheme=url_parts.scheme, host=url_parts.netloc)

    return response


def getDidHistoryAsync(did, url="http://localhost:8080"):
    url_parts = urlparse(url)

    path = "history/" + did

    response = yield from patronHelper(scheme=url_parts.scheme, host=url_parts.netloc, path=path)

    return response


def postHistoryAsync(data, sk, url="http://localhost:8080"):
    url_parts = urlparse(url)

    data['changed'] = str(arrow.utcnow())

    bdata = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode()

    headers = {
        "Signature": 'signer="{0}"'.format(gen.signResource(bdata, gen.key64uToKey(sk)))
    }

    response = yield from patronHelper(method="POST", scheme=url_parts.scheme, host=url_parts.netloc, data=data, headers=headers)

    return response


def putHistoryAsync(did, data, sk, psk, url="http://localhost:8080"):
    url_parts = urlparse(url)
    path = "{0}/{1}".format("history", did)

    data['changed'] = str(arrow.utcnow())

    bdata = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode()

    headers = {
        "Signature": 'signer="{0}"; rotation="{1}"'.format(
            gen.signResource(bdata, gen.key64uToKey(sk)),
            gen.signResource(bdata, gen.key64uToKey(psk))
        )
    }

    response = yield from patronHelper(method="PUT", scheme=url_parts.scheme, host=url_parts.netloc, path=path, data=data, headers=headers)

    return response
