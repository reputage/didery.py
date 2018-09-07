try:
    import simplejson as json
except ImportError:
    import json

from pydidery.help import consensing
from pydidery.help import signing
from pydidery.lib import generating as gen
from pydidery.models import responding as resp


HISTORY = 0
VK1 = 1
SK1 = 2
VK2 = 3
SK2 = 4


def testValidateDataInvalidSigsIncompleteMajority():
    consense = consensing.Consense()
    datum1 = gen.historyGen()  # (history, vk1, sk1, vk2, sk2)
    datum2 = gen.historyGen()

    bHistory1 = json.dumps(datum1[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()
    bHistory2 = json.dumps(datum2[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()
    datum1_sig = signing.signResource(bHistory1, gen.key64uToKey(datum1[SK1]))
    bad_sig = signing.signResource(bHistory2, gen.key64uToKey(datum1[SK1]))

    data = {
        "http://localhost:8000/history": resp.responseFactory(
            "http://localhost:8000/history",
            200,
            {
                "history": datum1[HISTORY],
                "signatures": {
                    "signer": bad_sig
                }
            }
        ),
        "http://localhost:8080/history": resp.responseFactory(
            "http://localhost:8080/history",
            200,
            {
                "history": datum1[HISTORY],
                "signatures": {
                    "signer": datum1_sig
                }
            }
        )
    }

    consense.validateData(data)

    assert consense.valid_data == {
        datum1_sig: {
            "history": datum1[HISTORY],
            "signatures": {
                "signer": datum1_sig
            }
        }
    }
    assert consense.valid_match_counts == {
        datum1_sig: 1
    }


def testValidateDataEmptyData():
    consense = consensing.Consense()
    consense.validateData({})

    assert consense.valid_data == {}
    assert consense.valid_match_counts == {}


def testValidateDataMajorityPasses():
    consense = consensing.Consense()
    datum1 = gen.historyGen()  # (history, vk1, sk1, vk2, sk2)
    datum2 = gen.historyGen()

    # Test Invalid signature causing incomplete majority
    bHistory1 = json.dumps(datum1[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()
    bHistory2 = json.dumps(datum2[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()
    datum1_sig = signing.signResource(bHistory1, gen.key64uToKey(datum1[SK1]))
    bad_sig = signing.signResource(bHistory2, gen.key64uToKey(datum1[SK1]))

    data = {
        "http://localhost:8000/history": resp.responseFactory(
            "http://localhost:8000/history",
            200,
            {
                "history": datum1[HISTORY],
                "signatures": {
                    "signer": bad_sig
                }
            }
        ),
        "http://localhost:8080/history": resp.responseFactory(
            "http://localhost:8080/history",
            200,
            {
                "history": datum1[HISTORY],
                "signatures": {
                    "signer": datum1_sig
                }
            }
        ),
        "http://localhost:8081/history": resp.responseFactory(
            "http://localhost:8081/history",
            200,
            {
                "history": datum1[HISTORY],
                "signatures": {
                    "signer": datum1_sig
                }
            }
        )
    }

    consense.validateData(data)

    assert consense.valid_data == {
        datum1_sig: {
            "history": datum1[HISTORY],
            "signatures": {
                "signer": datum1_sig
            }
        }
    }
    assert datum1_sig in consense.valid_match_counts
    assert consense.valid_match_counts[datum1_sig] == 2


def testValidateDataMultiSigData():
    consense = consensing.Consense()
    datum1 = gen.historyGen()  # (history, vk1, sk1, vk2, sk2)
    datum2 = gen.historyGen()

    vk, sk, did = gen.keyGen()
    datum1[HISTORY]["signer"] = 1
    datum1[HISTORY]["signers"].append(vk)

    bHistory1 = json.dumps(datum1[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()
    bHistory2 = json.dumps(datum2[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()
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
    assert datum1_sig in consense.valid_match_counts
    assert consense.valid_match_counts[datum1_sig] == 2


def testValidateDataValidSigsConflictingData():
    consense = consensing.Consense()
    datum1 = gen.historyGen()  # (history, vk1, sk1, vk2, sk2)
    datum2 = gen.historyGen()

    bHistory1 = json.dumps(datum1[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()
    bHistory2 = json.dumps(datum2[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()
    datum1_sig = signing.signResource(bHistory1, gen.key64uToKey(datum1[SK1]))
    datum2_sig = signing.signResource(bHistory2, gen.key64uToKey(datum2[SK1]))

    data = {
        "http://localhost:8000/history": resp.responseFactory(
            "http://localhost:8000/history",
            200,
            {
                "history": datum2[HISTORY],
                "signatures": {
                    "signer": datum2_sig
                }
            }
        ),
        "http://localhost:8080/history": resp.responseFactory(
            "http://localhost:8080/history",
            200,
            {
                "history": datum1[HISTORY],
                "signatures": {
                    "signer": datum1_sig
                }
            }
        ),
        "http://localhost:8081/history": resp.responseFactory(
            "http://localhost:8081/history",
            200,
            {
                "history": datum1[HISTORY],
                "signatures": {
                    "signer": datum1_sig
                }
            }
        )
    }

    consense.validateData(data)

    assert consense.valid_data == {
        datum1_sig: {
            "history": datum1[HISTORY],
            "signatures": {
                "signer": datum1_sig
            }
        },
        datum2_sig: {
            "history": datum2[HISTORY],
            "signatures": {
                "signer": datum2_sig
            }
        }
    }
    assert datum1_sig in consense.valid_match_counts
    assert consense.valid_match_counts[datum1_sig] == 2
    assert datum2_sig in consense.valid_match_counts
    assert consense.valid_match_counts[datum2_sig] == 1


def testValidateDataIncompleteMajority():
    consense = consensing.Consense()
    datum1 = gen.historyGen()  # (history, vk1, sk1, vk2, sk2)
    datum2 = gen.historyGen()

    bHistory1 = json.dumps(datum1[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()
    bHistory2 = json.dumps(datum2[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()
    datum1_sig = signing.signResource(bHistory1, gen.key64uToKey(datum1[SK1]))
    datum2_sig = signing.signResource(bHistory2, gen.key64uToKey(datum2[SK1]))

    data = {
        "http://localhost:8000/history": resp.responseFactory(
            "http://localhost:8000/history",
            200,
            {
                "history": datum2[HISTORY],
                "signatures": {
                    "signer": datum2_sig
                }
            }
        ),
        "http://localhost:8080/history": resp.responseFactory(
            "http://localhost:8080/history",
            200,
            {
                "history": datum1[HISTORY],
                "signatures": {
                    "signer": datum1_sig
                }
            }
        ),
        "http://localhost:8081/history": resp.responseFactory(
            "http://localhost:8081/history",
            200,
            {
                "history": datum1[HISTORY],
                "signatures": {
                    "signer": datum1_sig
                }
            }
        ),
        "http://localhost:8001/history": resp.responseFactory(
            "http://localhost:8001/history",
            200,
            {
                "history": datum2[HISTORY],
                "signatures": {
                    "signer": datum2_sig
                }
            }
        )
    }

    consense.validateData(data)

    assert consense.valid_data == {
        datum1_sig: {
            "history": datum1[HISTORY],
            "signatures": {
                "signer": datum1_sig
            }
        },
        datum2_sig: {
            "history": datum2[HISTORY],
            "signatures": {
                "signer": datum2_sig
            }
        }
    }
    assert datum1_sig in consense.valid_match_counts
    assert consense.valid_match_counts[datum1_sig] == 2
    assert datum2_sig in consense.valid_match_counts
    assert consense.valid_match_counts[datum2_sig] == 2


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


def testConsenseIncompleteMajority():
    consense = consensing.Consense()
    datum1 = gen.historyGen()  # (history, vk1, sk1, vk2, sk2)
    datum2 = gen.historyGen()

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


def testConsenseAllEqual():
    consense = consensing.Consense()
    datum1 = gen.historyGen()  # (history, vk1, sk1, vk2, sk2)

    vk, sk, did = gen.keyGen()
    datum1[HISTORY]["signer"] = 1
    datum1[HISTORY]["signers"].append(vk)

    bHistory1 = json.dumps(datum1[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()

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


def test50_50Split():
    consense = consensing.Consense()
    datum1 = gen.historyGen()  # (history, vk1, sk1, vk2, sk2)
    datum2 = gen.historyGen()

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


def testValidateDataWithHTTPError():
    consense = consensing.Consense()
    datum1 = gen.historyGen()  # (history, vk1, sk1, vk2, sk2)

    bHistory1 = json.dumps(datum1[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()
    datum1_sig = signing.signResource(bHistory1, gen.key64uToKey(datum1[SK1]))

    data = {
        "http://localhost:8000/history": resp.responseFactory(
            "http://localhost:8000/history",
            400,
            {}
        ),
        "http://localhost:8080/history": resp.responseFactory(
            "http://localhost:8080/history",
            200,
            {
                "history": datum1[HISTORY],
                "signatures": {
                    "signer": datum1_sig
                }
            }
        )
    }

    consense.validateData(data)

    assert consense.valid_data == {
        datum1_sig: {
            "history": datum1[HISTORY],
            "signatures": {
                "signer": datum1_sig
            }
        }
    }
    assert consense.valid_match_counts == {
        datum1_sig: 1
    }


def testValidateDataWithTimeOut():
    consense = consensing.Consense()
    datum1 = gen.historyGen()  # (history, vk1, sk1, vk2, sk2)

    bHistory1 = json.dumps(datum1[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()
    datum1_sig = signing.signResource(bHistory1, gen.key64uToKey(datum1[SK1]))

    data = {
        "http://localhost:8000/history": resp.responseFactory(
            "http://localhost:8000/history",
            0,
            {}
        ),
        "http://localhost:8080/history": resp.responseFactory(
            "http://localhost:8080/history",
            200,
            {
                "history": datum1[HISTORY],
                "signatures": {
                    "signer": datum1_sig
                }
            }
        )
    }

    consense.validateData(data)

    assert consense.valid_data == {
        datum1_sig: {
            "history": datum1[HISTORY],
            "signatures": {
                "signer": datum1_sig
            }
        }
    }
    assert consense.valid_match_counts == {
        datum1_sig: 1
    }
