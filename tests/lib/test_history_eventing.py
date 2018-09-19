import pytest

from diderypy.lib import history_eventing as event
from diderypy.lib import generating as gen
from diderypy.lib import historying as hist


history, vk1, sk1, vk2, sk2 = gen.historyGen()
vk3, sk3, did3 = gen.keyGen()
did = history['id']

urls = ["http://localhost:8080", "http://localhost:8000"]


def testGetNonExistentHistoryEvents():
    data, results = event.getHistoryEvents(did, urls)

    url1 = "http://localhost:8080/event/{}".format(did)
    url2 = "http://localhost:8000/event/{}".format(did)

    assert data is None
    assert len(results) == 2
    assert url1 in results
    assert url2 in results
    assert results[url1].response.data == {'title': '404 Not Found'}
    assert results[url2].response.data == {'title': '404 Not Found'}


def testGetHistoryEvents():
    events = {"events": {}}

    events['events']['0'] = hist.postHistory(history, sk1, urls).popitem()[1].response.data

    history['signer'] = 1
    history['signers'].append(vk3)

    events['events']['1'] = hist.putHistory(history, sk1, sk2, urls).popitem()[1].response.data

    data, results = event.getHistoryEvents(did, urls)
    assert data == events


def testGetHistoryEventsNoUrls():
    with pytest.raises(ValueError) as ex:
        event.getHistoryEvents(did, None)


def testGetHistoryEventsEmptyUrls():
    with pytest.raises(ValueError) as ex:
        event.getHistoryEvents(did, [])
