try:
    import simplejson as json
except ImportError:
    import json

from diderypy.help import consensing
from diderypy.help import signing
from diderypy.lib import generating as gen
from diderypy.models import responding as resp
from diderypy.models import consensing as consenseModel


HISTORY = 0
VK1 = 1
SK1 = 2
VK2 = 3
SK2 = 4


def testConsenseResults():
    consense = consensing.Consense()
    datum1 = gen.historyGen()  # (history, vk1, sk1, vk2, sk2)
    datum2 = gen.historyGen()

    # Test simple majority
    vk, sk, did = gen.keyGen()
    datum1[HISTORY]["signer"] = 1
    datum1[HISTORY]["signers"].append(vk)

    bHistory1 = json.dumps(datum1[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()
    bHistory2 = json.dumps(datum2[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()

    data = {
        "http://localhost:8000/history": resp.responseFactory(
            "http://localhost:8000/history",
            200,
            {
                "history": datum2[HISTORY],
                "signatures": {
                    "signer": signing.signResource(bHistory2, gen.key64uToKey(datum2[SK1]))
                }
            }
        ),
        "http://localhost:8080/history": resp.responseFactory(
            "http://localhost:8080/history",
            200,
            {
                "history": datum1[HISTORY],
                "signatures": {
                    "signer": signing.signResource(bHistory1, gen.key64uToKey(datum1[SK1])),
                    "rotation": signing.signResource(bHistory1, gen.key64uToKey(datum1[SK2]))
                }
            }
        ),
        "http://localhost:8081/history": resp.responseFactory(
            "http://localhost:8081/history",
            200,
            {
                "history": datum1[HISTORY],
                "signatures": {
                    "signer": signing.signResource(bHistory1, gen.key64uToKey(datum1[SK1])),
                    "rotation": signing.signResource(bHistory1, gen.key64uToKey(datum1[SK2]))
                }
            }
        )
    }

    results = consense.consense(data)[1]
    urls = ["http://localhost:8000/history", "http://localhost:8080/history", "http://localhost:8081/history"]

    assert len(results) == 3
    for url in urls:
        assert url in results

    exp_results = {
        "http://localhost:8000/history": consenseModel.ConsensusResult.VALID,
        "http://localhost:8080/history": consenseModel.ConsensusResult.VALID,
        "http://localhost:8081/history": consenseModel.ConsensusResult.VALID
    }

    for url, status in exp_results.items():
        assert results[url].validation_status == status

    # Test failed signature validation
    consense = consensing.Consense()
    data["http://localhost:8000/history"] = resp.responseFactory(
        "http://localhost:8000/history",
        200,
        {
            "history": datum2[HISTORY],
            "signatures": {
                "signer": signing.signResource(bHistory2, gen.key64uToKey(datum2[SK2]))
            }
        }
    )

    results = consense.consense(data)[1]

    assert len(results) == 3
    for url in urls:
        assert url in results

    exp_results["http://localhost:8000/history"] = consenseModel.ConsensusResult.FAILED

    for url, status in exp_results.items():
        assert results[url].validation_status == status

    # Test failed request
    consense = consensing.Consense()
    data["http://localhost:8000/history"] = resp.responseFactory(
        "http://localhost:8000/history",
        400,
        {
            "history": datum2[HISTORY],
            "signatures": {
                "signer": signing.signResource(bHistory2, gen.key64uToKey(datum2[SK1]))
            }
        }
    )

    results = consense.consense(data)[1]

    assert len(results) == 3
    for url in urls:
        assert url in results

    exp_results["http://localhost:8000/history"] = consenseModel.ConsensusResult.ERROR

    for url, status in exp_results.items():
        assert results[url].validation_status == status