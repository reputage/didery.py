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


def testValidateSignatures():
    VALID_DATA = 0
    SIG_COUNTS = 1
    datum1 = gen.historyGen()  # (history, vk1, sk1, vk2, sk2)
    datum2 = gen.historyGen()

    # Test Invalid signature causing incomplete majority
    bHistory1 = json.dumps(datum1[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()
    bHistory2 = json.dumps(datum2[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()
    datum1_sig = gen.signResource(bHistory1, gen.key64uToKey(datum1[SK1]))
    data = [
        {
            "history": datum1[HISTORY],
            "signatures": [
                gen.signResource(bHistory2, gen.key64uToKey(datum1[SK1]))
            ]
        },
        {
            "history": datum1[HISTORY],
            "signatures": [
                datum1_sig
            ]
        }
    ]

    result = consensing.validateHistorySignatures(data)
    assert result[VALID_DATA] is None
    assert result[SIG_COUNTS] is None

    # Test empty data
    result = consensing.validateHistorySignatures({})
    assert result[VALID_DATA] is None
    assert result[SIG_COUNTS] is None

    # Test that majority of valid data passes
    data.append(
        {
            "history": datum1[HISTORY],
            "signatures": [
                datum1_sig
            ]
        }
    )

    result = consensing.validateHistorySignatures(data)
    assert result[VALID_DATA] is not None
    assert datum1_sig in result[SIG_COUNTS]
    assert result[SIG_COUNTS][datum1_sig] == 2

    # Test multiple signatures
    vk, sk = gen.keyGen()
    datum1[HISTORY]["signer"] = 1
    datum1[HISTORY]["signers"].append(vk)

    bHistory1 = json.dumps(datum1[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()
    datum1_sig = gen.signResource(bHistory1, gen.key64uToKey(datum1[SK2]))
    data = [
        {
            "history": datum1[HISTORY],
            "signatures": [
                gen.signResource(bHistory2, gen.key64uToKey(datum1[SK1])),
                gen.signResource(bHistory2, gen.key64uToKey(datum1[SK2]))
            ]
        },
        {
            "history": datum1[HISTORY],
            "signatures": [
                gen.signResource(bHistory1, gen.key64uToKey(datum1[SK1])),
                datum1_sig
            ]
        },
        {
            "history": datum1[HISTORY],
            "signatures": [
                gen.signResource(bHistory1, gen.key64uToKey(datum1[SK1])),
                datum1_sig
            ]
        }
    ]

    result = consensing.validateHistorySignatures(data)
    assert result[VALID_DATA] is not None
    assert datum1_sig in result[SIG_COUNTS]
    assert result[SIG_COUNTS][datum1_sig] == 2

    # Test all valid signatures, but conflicting data
    datum2_sig = gen.signResource(bHistory2, gen.key64uToKey(datum2[SK1]))
    data[0] = {
        "history": datum2[HISTORY],
        "signatures": [
            datum2_sig
        ]
    }

    result = consensing.validateHistorySignatures(data)
    assert result[VALID_DATA] is not None
    assert datum1_sig in result[SIG_COUNTS]
    assert result[SIG_COUNTS][datum1_sig] == 2
    assert datum2_sig in result[SIG_COUNTS]
    assert result[SIG_COUNTS][datum2_sig] == 1


def testConsenseHistory():
    datum1 = gen.historyGen()  # (history, vk1, sk1, vk2, sk2)
    datum2 = gen.historyGen()

    # Test simple majority
    vk, sk = gen.keyGen()
    datum1[HISTORY]["signer"] = 1
    datum1[HISTORY]["signers"].append(vk)

    bHistory1 = json.dumps(datum1[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()
    bHistory2 = json.dumps(datum2[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()
    data = [
        {
            "history": datum2[HISTORY],
            "signatures": [
                gen.signResource(bHistory2, gen.key64uToKey(datum2[SK1]))
            ]
        },
        {
            "history": datum1[HISTORY],
            "signatures": [
                gen.signResource(bHistory1, gen.key64uToKey(datum1[SK1])),
                gen.signResource(bHistory1, gen.key64uToKey(datum1[SK2]))
            ]
        },
        {
            "history": datum1[HISTORY],
            "signatures": [
                gen.signResource(bHistory1, gen.key64uToKey(datum1[SK1])),
                gen.signResource(bHistory1, gen.key64uToKey(datum1[SK2]))
            ]
        }
    ]

    assert consensing.consense(data) is not None

    # Test incomplete majority
    data = [
        {
            "history": datum2[HISTORY],
            "signatures": [
                gen.signResource(bHistory2, gen.key64uToKey(datum2[SK1]))
            ]
        },
        {
            "history": gen.historyGen()[HISTORY],
            "signatures": [
                gen.signResource(bHistory1, gen.key64uToKey(datum2[SK1]))
            ]
        },
        {
            "history": datum1[HISTORY],
            "signatures": [
                gen.signResource(bHistory1, gen.key64uToKey(datum1[SK1])),
                gen.signResource(bHistory1, gen.key64uToKey(datum1[SK2]))
            ]
        }
    ]

    assert consensing.consense(data) is None

    # Test all equal
    data = [
        {
            "history": datum1[HISTORY],
            "signatures": [
                gen.signResource(bHistory1, gen.key64uToKey(datum1[SK1])),
                gen.signResource(bHistory1, gen.key64uToKey(datum1[SK2]))
            ]
        },
        {
            "history": datum1[HISTORY],
            "signatures": [
                gen.signResource(bHistory1, gen.key64uToKey(datum1[SK1])),
                gen.signResource(bHistory1, gen.key64uToKey(datum1[SK2]))
            ]
        },
        {
            "history": datum1[HISTORY],
            "signatures": [
                gen.signResource(bHistory1, gen.key64uToKey(datum1[SK1])),
                gen.signResource(bHistory1, gen.key64uToKey(datum1[SK2]))
            ]
        }
    ]

    assert consensing.consense(data) == {
            "history": datum1[HISTORY],
            "signatures": [
                gen.signResource(bHistory1, gen.key64uToKey(datum1[SK1])),
                gen.signResource(bHistory1, gen.key64uToKey(datum1[SK2]))
            ]
        }
