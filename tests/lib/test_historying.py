import pytest

try:
    import simplejson as json
except ImportError:
    import json

from ioflo.aio.http import Valet

# import didery.routing

from diderypy.help import helping as h
from diderypy.lib import generating as gen
from diderypy.lib import historying as hist

history, vk1, sk1, vk2, sk2 = gen.historyGen()
vk3, sk3, did3 = gen.keyGen()
did = history['id']

url1, url2 = "http://localhost:8080/history", "http://localhost:8000/history"
urls = ["http://localhost:8080", "http://localhost:8000"]


def testPostHistory():
    result = hist.postHistory(history, sk1, urls)

    assert result[url1].status == 201
    assert result[url2].status == 201


def testPostHistoryNoUrls():
    with pytest.raises(ValueError) as ex:
        hist.postHistory(history, sk1, None)


def testPostHistoryEmptyUrls():
    with pytest.raises(ValueError) as ex:
        hist.postHistory(history, sk1, [])


def testPostHistoryNoSk():
    with pytest.raises(ValueError) as ex:
        hist.postHistory(history, None, urls)


def testPostHistoryEmptySk():
    with pytest.raises(ValueError) as ex:
        hist.postHistory(history, "", urls)


def testGetHistory():
    data, results = hist.getHistory(did, urls)

    assert data['history'] == history


def testGetHistoryNoUrls():
    with pytest.raises(ValueError) as ex:
        hist.getHistory(did, None)


def testGetHistoryEmptyUrls():
    with pytest.raises(ValueError) as ex:
        hist.getHistory(did, [])


def testPutHistory():
    history['signer'] = 1
    history['signers'].append(vk3)

    result = hist.putHistory(history, sk1, sk2, urls)

    assert result[url1+"/"+history["id"]].status == 200
    assert result[url1+"/"+history["id"]].response.body == history
    assert result[url2+"/"+history["id"]].status == 200
    assert result[url2+"/"+history["id"]].response.body == history


def testPutHistoryNoUrls():
    with pytest.raises(ValueError) as ex:
        hist.putHistory(history, sk1, sk2, None)


def testPutHistoryEmptyUrls():
    with pytest.raises(ValueError) as ex:
        hist.putHistory(history, sk1, sk2, [])


def testPutHistoryNoSk():
    with pytest.raises(ValueError) as ex:
        hist.putHistory(history, None, sk2, urls)


def testPutHistoryEmptySk():
    with pytest.raises(ValueError) as ex:
        hist.putHistory(history, "", sk2, urls)


def testPutHistoryNoPsk():
    with pytest.raises(ValueError) as ex:
        hist.putHistory(history, sk1, None, urls)


def testPutHistoryEmptyPsk():
    with pytest.raises(ValueError) as ex:
        hist.putHistory(history, sk1, "", urls)


def testDeleteHistory():
    result = hist.deleteHistory(did, sk2, urls)

    assert result[url1+"/"+did].status == 200
    assert result[url1+"/"+did].response.body == history
    assert result[url2+"/"+did].status == 200
    assert result[url2+"/"+did].response.body == history


def testDeleteHistoryNoUrls():
    with pytest.raises(ValueError) as ex:
        hist.deleteHistory(did, sk2, None)


def testDeleteHistoryEmptyUrls():
    with pytest.raises(ValueError) as ex:
        hist.deleteHistory(did, sk2, [])


def testDeleteHistoryNoSk():
    with pytest.raises(ValueError) as ex:
        hist.deleteHistory(did, None, urls)


def testDeleteHistoryEmptySk():
    with pytest.raises(ValueError) as ex:
        hist.deleteHistory(did, "", urls)
