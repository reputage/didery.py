try:
    import simplejson as json
except ImportError:
    import json

from pydidery.help import consensing
from pydidery.lib import generating as gen


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
#     datum_sig = gen.signResource(bHistory1, gen.key64uToKey(datum[SK1]))
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
    VALID_DATA = 0
    SIG_COUNTS = 1
    datum1 = gen.historyGen()  # (history, vk1, sk1, vk2, sk2)
    datum2 = gen.historyGen()

    # Test Invalid signature causing incomplete majority
    bHistory1 = json.dumps(datum1[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()
    bHistory2 = json.dumps(datum2[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()
    datum1_sig = gen.signResource(bHistory1, gen.key64uToKey(datum1[SK1]))
    data = {
        "http://localhost:8000": ({
            "history": datum1[HISTORY],
            "signatures": {
                "signer": gen.signResource(bHistory2, gen.key64uToKey(datum1[SK1]))
            }
        }, 200),
        "http://localhost:8080": ({
            "history": datum1[HISTORY],
            "signatures": {
                "signer": datum1_sig
            }
        }, 200)
    }

    result = consensing.validateSignatures(data, "history")
    assert result[VALID_DATA] is None
    assert result[SIG_COUNTS] is None

    # Test empty data
    result = consensing.validateSignatures({}, "history")
    assert result[VALID_DATA] == {}
    assert result[SIG_COUNTS] == {}

    # Test that majority of valid data passes
    data["http://localhost:8081"] = (
        {
            "history": datum1[HISTORY],
            "signatures": {
                "signer": datum1_sig
            }
        },
        200
    )

    print("RESULTS:                   !")
    print(bHistory1)
    result = consensing.validateSignatures(data, "history")

    assert result[VALID_DATA] is not None
    assert datum1_sig in result[SIG_COUNTS]
    assert result[SIG_COUNTS][datum1_sig] == 2

    # Test multiple signatures
    vk, sk = gen.keyGen()
    datum1[HISTORY]["signer"] = 1
    datum1[HISTORY]["signers"].append(vk)

    bHistory1 = json.dumps(datum1[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()
    datum1_sig = gen.signResource(bHistory1, gen.key64uToKey(datum1[SK2]))
    data = {
        "http://localhost:8000": ({
            "history": datum1[HISTORY],
            "signatures": {
                "signer": gen.signResource(bHistory2, gen.key64uToKey(datum1[SK1])),
                "rotation": gen.signResource(bHistory2, gen.key64uToKey(datum1[SK2]))
            }
        }, 200),
        "http://localhost:8080": ({
            "history": datum1[HISTORY],
            "signatures": {
                "signer": gen.signResource(bHistory1, gen.key64uToKey(datum1[SK1])),
                "rotation": datum1_sig
            }
        }, 200),
        "http://localhost:8081": ({
            "history": datum1[HISTORY],
            "signatures": {
                "signer": gen.signResource(bHistory1, gen.key64uToKey(datum1[SK1])),
                "rotation": datum1_sig
            }
        }, 200)
    }

    result = consensing.validateSignatures(data, "history")
    assert result[VALID_DATA] is not None
    assert datum1_sig in result[SIG_COUNTS]
    assert result[SIG_COUNTS][datum1_sig] == 2

    # Test all valid signatures, but conflicting data
    datum2_sig = gen.signResource(bHistory2, gen.key64uToKey(datum2[SK1]))
    data["http://localhost:8000"] = ({
        "history": datum2[HISTORY],
        "signatures": {
            "signer": datum2_sig
        }
    }, 200)

    result = consensing.validateSignatures(data, "history")
    assert result[VALID_DATA] is not None
    assert datum1_sig in result[SIG_COUNTS]
    assert result[SIG_COUNTS][datum1_sig] == 2
    assert datum2_sig in result[SIG_COUNTS]
    assert result[SIG_COUNTS][datum2_sig] == 1


def testConsense():
    datum1 = gen.historyGen()  # (history, vk1, sk1, vk2, sk2)
    datum2 = gen.historyGen()

    # Test simple majority
    vk, sk = gen.keyGen()
    datum1[HISTORY]["signer"] = 1
    datum1[HISTORY]["signers"].append(vk)

    bHistory1 = json.dumps(datum1[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()
    bHistory2 = json.dumps(datum2[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()
    data = {
        "http://localhost:8000": ({
            "history": datum2[HISTORY],
            "signatures": {
                "signer": gen.signResource(bHistory2, gen.key64uToKey(datum2[SK1]))
            }
        }, 200),
        "http://localhost:8080": ({
            "history": datum1[HISTORY],
            "signatures": {
                "signer": gen.signResource(bHistory1, gen.key64uToKey(datum1[SK1])),
                "rotation": gen.signResource(bHistory1, gen.key64uToKey(datum1[SK2]))
            }
        }, 200),
        "http://localhost:8081": ({
            "history": datum1[HISTORY],
            "signatures": {
                "signer": gen.signResource(bHistory1, gen.key64uToKey(datum1[SK1])),
                "rotation": gen.signResource(bHistory1, gen.key64uToKey(datum1[SK2]))
            }
        }, 200)
    }

    assert consensing.consense(data)[0] is not None

    # Test incomplete majority
    data = {
        "http://localhost:8000": ({
            "history": datum2[HISTORY],
            "signatures": {
                "signer": gen.signResource(bHistory2, gen.key64uToKey(datum2[SK1]))
            }
        }, 200),
        "http://localhost:8080": ({
            "history": gen.historyGen()[HISTORY],
            "signatures": {
                "signer": gen.signResource(bHistory1, gen.key64uToKey(datum2[SK1]))
            }
        }, 200),
        "http://localhost:8081": ({
            "history": datum1[HISTORY],
            "signatures": {
                "signer": gen.signResource(bHistory1, gen.key64uToKey(datum1[SK1])),
                "rotation": gen.signResource(bHistory1, gen.key64uToKey(datum1[SK2]))
            }
        }, 200)
    }

    print(consensing.consense(data))
    assert consensing.consense(data)[0] is None

    # Test all equal
    data = {
        "http://localhost:8000": ({
            "history": datum1[HISTORY],
            "signatures": {
                "signer": gen.signResource(bHistory1, gen.key64uToKey(datum1[SK1])),
                "rotation": gen.signResource(bHistory1, gen.key64uToKey(datum1[SK2]))
            }
        }, 200),
        "http://localhost:8080": ({
            "history": datum1[HISTORY],
            "signatures": {
                "signer": gen.signResource(bHistory1, gen.key64uToKey(datum1[SK1])),
                "rotation": gen.signResource(bHistory1, gen.key64uToKey(datum1[SK2]))
            }
        }, 200),
        "http://localhost:8081": ({
            "history": datum1[HISTORY],
            "signatures": {
                "signer": gen.signResource(bHistory1, gen.key64uToKey(datum1[SK1])),
                "rotation": gen.signResource(bHistory1, gen.key64uToKey(datum1[SK2]))
            }
        }, 200)
    }

    assert consensing.consense(data)[0] == {
            "history": datum1[HISTORY],
            "signatures": {
                "signer": gen.signResource(bHistory1, gen.key64uToKey(datum1[SK1])),
                "rotation": gen.signResource(bHistory1, gen.key64uToKey(datum1[SK2]))
            }
        }
