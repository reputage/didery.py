import arrow

try:
    import simplejson as json
except ImportError:
    import json

from ioflo.aio.http import Valet

# import didery.routing

from pydidery.help import helping as h
from pydidery.lib import generating as gen
from pydidery.lib import historying as hist

history, vk1, sk1, vk2, sk2 = gen.historyGen()
vk3, sk3 = gen.keyGen()
did = history['id']

url1, url2 = "http://localhost:8080", "http://localhost:8000"
urls = ["http://localhost:8080", "http://localhost:8000"]


def testPostHistory():
    result = hist.postHistory(history, sk1, urls)

    assert result[url1][1] == 201
    assert result[url2][1] == 201


def testGetHistory():
    result = hist.getHistory(did, urls)

    assert result['history'] == history


def testPutHistory():
    history['signer'] = 1
    history['signers'].append(vk3)

    result = hist.putHistory(history, sk1, sk2, urls)

    assert result[url1][1] == 200
    assert result[url1][0]["history"] == history
    assert result[url2][1] == 200
    assert result[url2][0]["history"] == history


def testDeleteHistory():
    result = hist.deleteHistory(did, sk2, urls)

    assert result[url1][1] == 200
    assert result[url1][0]["deleted"]["history"] == history
    assert result[url2][1] == 200
    assert result[url2][0]["deleted"]["history"] == history
