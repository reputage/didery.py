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


def testGetAllHistories():
    result = hist.getAllHistories()

    assert result[0] == '{}'


def testPostHistory():
    result = hist.postHistory(history, sk1)

    assert result[1] == 201


def testGetDidHistory():
    result = hist.getDidHistory(did)

    assert result[1] == 200
    assert json.loads(result[0])['history'] == history


def testPutHistory():
    history['signer'] = 1
    history['signers'].append(vk3)

    result = hist.putHistory(did,history, sk1, sk2)

    print(result)
    assert result[1] == 200
