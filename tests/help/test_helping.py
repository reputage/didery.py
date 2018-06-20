import pytest
import asyncio
import aiohttp
from asyncio import ensure_future
import arrow

try:
    import simplejson as json
except ImportError:
    import json

from ioflo.aio.http import httping

from pydidery.help import helping as h
from pydidery.lib import generating as gen


async def helper():
    async with aiohttp.ClientSession() as session:
        async with session.get("http://localhost:8080/history") as response:
            data = await response.text()
            # print(data)
            return data


async def httpPost(url, data, headers):
    async with aiohttp.ClientSession(json_serialize=json.dumps) as session:
        async with session.post(url, json=data, headers=headers) as response:
            status = response.status
            data = await response.text()

            return status, data


def paetronHelper():
    result = yield from h.httpRequest("GET", host="localhost", port=8080, path="history")

    if result['status'] != 200:
        if result['errored']:
            emsg = result['error']
        else:
            emsg = "unknown"
        raise httping.HTTPError(berep['status'],
                                title="Backend Validation Error",
                                detail="Error backend validation. {}".format(emsg))

    print(result['body'].decode())

    return result['body'].decode()


def testHttpRequest():
    history, vk, sk, pvk, psk = gen.historyGen()
    history['changed'] = str(arrow.utcnow())
    did = history['id']
    url = "http://localhost:8080/history/" + did
    headers = {
        "Signature": 'signer="{0}"'.format(gen.signResource(json.dumps(history).encode('utf-8'), sk))
    }

    loop = asyncio.get_event_loop()
    test = loop.run_until_complete(httpPost(url, history, headers))

    print(test)

    loop = asyncio.get_event_loop()
    test = loop.run_until_complete(helper())

    print(test)

    assert False


def testPaetron():
    response = paetronHelper()

    while True:
        test = next(response)
        print(test)
        if not test:
            break

    # print(test)

    assert False
