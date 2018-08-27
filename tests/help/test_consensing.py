try:
    import simplejson as json
except ImportError:
    import json

from pydidery.help import consensing
from pydidery.help import signing
from pydidery.lib import generating as gen
from pydidery.models import responding as resp
from pydidery.models import consensing as consenseModel
from ..data import history_data_builder as builder


HISTORY = 0
VK1 = 1
SK1 = 2
VK2 = 3
SK2 = 4


# def test():
#     datum = gen.historyGen()  # (history, vk1, sk1, vk2, sk2)
#
#     # Test Invalid signature causing incomplete majority
#     bHistory1 = json.dumps(datum[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()
#     datum_sig = signing.signResource(bHistory1, gen.key64uToKey(datum[SK1]))
#     data = json.dumps({
#             "history": datum[HISTORY],
#             "signatures": {
#                 "signer": datum_sig
#             }
#         })
#
#     hist = consensing.HistoryData(data)
#
#     assert hist.did == datum[HISTORY]["id"]
#
#     hist.did = ""
#     assert hist.did == ""
#     assert hist.body["id"] == ""


def testvalidateSignatures():
    consense = consensing.Consense()
    datum1 = gen.historyGen()  # (history, vk1, sk1, vk2, sk2)
    datum2 = gen.historyGen()

    # Test Invalid signature causing incomplete majority
    bHistory1 = json.dumps(datum1[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()
    bHistory2 = json.dumps(datum2[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()
    datum1_sig = signing.signResource(bHistory1, gen.key64uToKey(datum1[SK1]))
    bad_sig = signing.signResource(bHistory2, gen.key64uToKey(datum1[SK1]))

    response1 = builder.DideryResponseBuilder(
        builder.SignedHistoryBuilder().withInvalidSignerSignature()
    ).withPort(8000)
    response2 = builder.DideryResponseBuilder(
        builder.SignedHistoryBuilder()
    )

    data = {
        "http://localhost:8000/history": response1.build(),
        "http://localhost:8080/history": response2.build()
    }

    consense.validateData(data)

    history2 = response2.history
    assert consense.valid_data == {
        history2.signerSig: builder.SignedHistoryBuilder().build()
    }
    assert consense.valid_sig_counts == {
        history2.signerSig: 1
    }

    # Test empty data
    consense = consensing.Consense()
    consense.validateData({})

    assert consense.valid_data == {}
    assert consense.valid_sig_counts == {}

    # Test that majority of valid data passes
    consense = consensing.Consense()
    response3 = builder.DideryResponseBuilder(
        builder.SignedHistoryBuilder()
    ).withPort(8081)
    data["http://localhost:8081/history"] = response3.build()
    consense.validateData(data)

    assert consense.valid_data == {
        history2.signerSig: builder.SignedHistoryBuilder().build()
    }
    assert history2.signerSig in consense.valid_sig_counts
    assert consense.valid_sig_counts[history2.signerSig] == 2

    # Test multiple signatures
    consense = consensing.Consense()
    vk, sk, did = gen.keyGen()
    datum1[HISTORY]["signer"] = 1
    datum1[HISTORY]["signers"].append(vk)

    bHistory1 = json.dumps(datum1[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()
    datum1_sig = signing.signResource(bHistory1, gen.key64uToKey(datum1[SK2]))

    data = {
        "http://localhost:8000/history": resp.responseFactory(
            "http://localhost:8000/history",
            200,
            {
                "history": datum1[HISTORY],
                "signatures": {
                    "signer": signing.signResource(bHistory2, gen.key64uToKey(datum1[SK1])),
                    "rotation": signing.signResource(bHistory2, gen.key64uToKey(datum1[SK2]))
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
                    "rotation": datum1_sig
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
                    "rotation": datum1_sig
                }
            }
        )
    }

    consense.validateData(data)

    assert consense.valid_data == {
        datum1_sig: {
            "history": datum1[HISTORY],
            "signatures": {
                "signer": signing.signResource(bHistory1, gen.key64uToKey(datum1[SK1])),
                "rotation": datum1_sig
            }
        }
    }
    assert datum1_sig in consense.valid_sig_counts
    assert consense.valid_sig_counts[datum1_sig] == 2

    # Test all valid signatures, but conflicting data
    consense = consensing.Consense()
    datum2_sig = signing.signResource(bHistory2, gen.key64uToKey(datum2[SK1]))
    data["http://localhost:8000/history"] = resp.responseFactory(
        "http://localhost:8000/history",
        200,
        {
            "history": datum2[HISTORY],
            "signatures": {
                "signer": datum2_sig
            }
        }
    )

    consense.validateData(data)

    assert consense.valid_data == {
        datum1_sig: {
            "history": datum1[HISTORY],
            "signatures": {
                "signer": signing.signResource(bHistory1, gen.key64uToKey(datum1[SK1])),
                "rotation": datum1_sig
            }
        },
        datum2_sig: {
            "history": datum2[HISTORY],
            "signatures": {
                "signer": datum2_sig
            }
        }
    }
    assert datum1_sig in consense.valid_sig_counts
    assert consense.valid_sig_counts[datum1_sig] == 2
    assert datum2_sig in consense.valid_sig_counts
    assert consense.valid_sig_counts[datum2_sig] == 1

    # Test all valid signatures but incomplete majority
    consense = consensing.Consense()
    data["http://localhost:8001/history"] = resp.responseFactory(
        "http://localhost:8001/history",
        200,
        {
            "history": datum2[HISTORY],
            "signatures": {
                "signer": datum2_sig
            }
        }
    )

    consense.validateData(data)

    assert consense.valid_data == {
        datum1_sig: {
            "history": datum1[HISTORY],
            "signatures": {
                "signer": signing.signResource(bHistory1, gen.key64uToKey(datum1[SK1])),
                "rotation": datum1_sig
            }
        },
        datum2_sig: {
            "history": datum2[HISTORY],
            "signatures": {
                "signer": datum2_sig
            }
        }
    }
    assert datum1_sig in consense.valid_sig_counts
    assert consense.valid_sig_counts[datum1_sig] == 2
    assert datum2_sig in consense.valid_sig_counts
    assert consense.valid_sig_counts[datum2_sig] == 2


def testConsense():
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

    assert consense.consense(data)[0] == {
            "history": datum1[HISTORY],
            "signatures": {
                "signer": signing.signResource(bHistory1, gen.key64uToKey(datum1[SK1])),
                "rotation": signing.signResource(bHistory1, gen.key64uToKey(datum1[SK2]))
            }
        }

    # Test incomplete majority
    consense = consensing.Consense()
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
                "history": gen.historyGen()[HISTORY],
                "signatures": {
                    "signer": signing.signResource(bHistory1, gen.key64uToKey(datum2[SK1]))
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

    assert consense.consense(data)[0] is None

    # Test all equal
    consense = consensing.Consense()
    data = {
        "http://localhost:8000/history": resp.responseFactory(
            "http://localhost:8000/history",
            200,
            {
                "history": datum1[HISTORY],
                "signatures": {
                    "signer": signing.signResource(bHistory1, gen.key64uToKey(datum1[SK1])),
                    "rotation": signing.signResource(bHistory1, gen.key64uToKey(datum1[SK2]))
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

    assert consense.consense(data)[0] == {
            "history": datum1[HISTORY],
            "signatures": {
                "signer": signing.signResource(bHistory1, gen.key64uToKey(datum1[SK1])),
                "rotation": signing.signResource(bHistory1, gen.key64uToKey(datum1[SK2]))
            }
        }

    # Test half and half
    consense = consensing.Consense()
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
        "http://localhost:8001/history": resp.responseFactory(
            "http://localhost:8001/history",
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

    assert consense.consense(data)[0] is None


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
        "http://localhost:8000/history": consenseModel.ConsensusResult.SUCCESS,
        "http://localhost:8080/history": consenseModel.ConsensusResult.SUCCESS,
        "http://localhost:8081/history": consenseModel.ConsensusResult.SUCCESS
    }

    for url, status in exp_results.items():
        assert results[url].req_status == status

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
        assert results[url].req_status == status

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
        assert results[url].req_status == status
