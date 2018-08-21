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

    assert result[url1]["http_status"] == 201
    assert result[url2]["http_status"] == 201


def testGetHistory():
    data, results = hist.getHistory(did, urls)

    assert data['history'] == history


def testPutHistory():
    history['signer'] = 1
    history['signers'].append(vk3)

    result = hist.putHistory(history, sk1, sk2, urls)

    assert result[url1]["http_status"] == 200
    assert result[url1]["data"]["history"] == history
    assert result[url2]["http_status"] == 200
    assert result[url2]["data"]["history"] == history


def testDeleteHistory():
    result = hist.deleteHistory(did, sk2, urls)

    assert result[url1]["http_status"] == 200
    assert result[url1]["data"]["deleted"]["history"] == history
    assert result[url2]["http_status"] == 200
    assert result[url2]["data"]["deleted"]["history"] == history
