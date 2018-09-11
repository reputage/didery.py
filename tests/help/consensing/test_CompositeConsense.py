from hashlib import sha256

try:
    import simplejson as json
except ImportError:
    import json

from copy import deepcopy
from collections import OrderedDict as ODict

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
    consense = consensing.CompositeConsense()
    history_inception = gen.historyGen()  # (history, vk1, sk1, vk2, sk2)
    url8000 = 'http://localhost:8000/event/{}'.format(history_inception[HISTORY]["id"])
    url8080 = 'http://localhost:8080/event/{}'.format(history_inception[HISTORY]["id"])
    bad_vk, bad_sk, bad_did = gen.keyGen()
    ppvk, ppsk, ppdid = gen.keyGen()
    history_rotation1 = deepcopy(history_inception)
    history_rotation1[HISTORY]["signers"].append(ppvk)
    history_rotation1[HISTORY]["signer"] = 1

    bHistory_inception = json.dumps(history_inception[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()
    bHistory_rotation = json.dumps(history_rotation1[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()
    inception_sig = signing.signResource(bHistory_inception, gen.key64uToKey(history_inception[SK1]))
    rotation1_sign_sig = signing.signResource(bHistory_rotation, gen.key64uToKey(history_inception[SK1]))
    rotation1_rot_sig = signing.signResource(bHistory_rotation, gen.key64uToKey(history_inception[SK2]))
    bad_sig = signing.signResource(bHistory_inception, gen.key64uToKey(bad_sk))

    data = {
        url8000:
            resp.DideryResponse(
                url8000,
                200,
                {
                    '1': resp.HistoryData(
                        {
                            "history": history_rotation1[HISTORY],
                            "signatures": {
                                "signer": rotation1_sign_sig,
                                "rotation": rotation1_rot_sig
                            }
                        }
                    ),
                    '0': resp.HistoryData(
                        {
                            "history": history_inception[HISTORY],
                            "signatures": {
                                "signer": inception_sig,
                            }
                        }
                    )
                }
            ),
        url8080:
            resp.DideryResponse(
                url8080,
                200,
                {
                    '1': resp.HistoryData(
                        {
                            "history": history_rotation1[HISTORY],
                            "signatures": {
                                "signer": rotation1_sign_sig,
                                "rotation": bad_sig
                            }
                        }
                    ),
                    '0': resp.HistoryData(
                        {
                            "history": history_inception[HISTORY],
                            "signatures": {
                                "signer": inception_sig,
                            }
                        }
                    )
                }
            )

    }

    consense.validateData(data)

    exp_data = {
        '1': resp.HistoryData(
            {
                "history": history_rotation1[HISTORY],
                "signatures": {
                    "signer": rotation1_sign_sig,
                    "rotation": rotation1_rot_sig
                }
            }
        ),
        '0': resp.HistoryData(
            {
                "history": history_inception[HISTORY],
                "signatures": {
                    "signer": inception_sig,
                }
            }
        )
    }
    sha = sha256(str(ODict(exp_data)).encode()).hexdigest()

    assert consense.valid_data == {
        sha: {
            '1': {
                "history": history_rotation1[HISTORY],
                "signatures": {
                    "signer": rotation1_sign_sig,
                    "rotation": rotation1_rot_sig
                }
            },
            '0': {
                "history": history_inception[HISTORY],
                "signatures": {
                    "signer": inception_sig,
                }
            }
        }
    }
    assert consense.valid_match_counts == {
        sha: 1
    }


def testValidateDataEmptyData():
    consense = consensing.CompositeConsense()
    consense.validateData({})

    assert consense.valid_data == {}
    assert consense.valid_match_counts == {}


def testValidateDataMajorityPasses():
    consense = consensing.CompositeConsense()
    history_inception = gen.historyGen()  # (history, vk1, sk1, vk2, sk2)
    url8000 = 'http://localhost:8000/event/{}'.format(history_inception[HISTORY]["id"])
    url8080 = 'http://localhost:8080/event/{}'.format(history_inception[HISTORY]["id"])
    url8081 = 'http://localhost:8081/event/{}'.format(history_inception[HISTORY]["id"])
    bad_vk, bad_sk, bad_did = gen.keyGen()
    ppvk, ppsk, ppdid = gen.keyGen()
    history_rotation1 = deepcopy(history_inception)
    history_rotation1[HISTORY]["signers"].append(ppvk)
    history_rotation1[HISTORY]["signer"] = 1

    bHistory_inception = json.dumps(history_inception[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()
    bHistory_rotation = json.dumps(history_rotation1[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()
    inception_sig = signing.signResource(bHistory_inception, gen.key64uToKey(history_inception[SK1]))
    rotation1_sign_sig = signing.signResource(bHistory_rotation, gen.key64uToKey(history_inception[SK1]))
    rotation1_rot_sig = signing.signResource(bHistory_rotation, gen.key64uToKey(history_inception[SK2]))
    bad_sig = signing.signResource(bHistory_inception, gen.key64uToKey(bad_sk))

    data = {
        url8000:
            resp.DideryResponse(
                url8000,
                200,
                {
                    '1': resp.HistoryData(
                        {
                            "history": history_rotation1[HISTORY],
                            "signatures": {
                                "signer": rotation1_sign_sig,
                                "rotation": rotation1_rot_sig
                            }
                        }
                    ),
                    '0': resp.HistoryData(
                        {
                            "history": history_inception[HISTORY],
                            "signatures": {
                                "signer": inception_sig,
                            }
                        }
                    )
                }
            ),
        url8080:
            resp.DideryResponse(
                url8080,
                200,
                {
                    '1': resp.HistoryData(
                        {
                            "history": history_rotation1[HISTORY],
                            "signatures": {
                                "signer": rotation1_sign_sig,
                                "rotation": bad_sig
                            }
                        }
                    ),
                    '0': resp.HistoryData(
                        {
                            "history": history_inception[HISTORY],
                            "signatures": {
                                "signer": inception_sig,
                            }
                        }
                    )
                }
            ),
        url8081:
            resp.DideryResponse(
                url8081,
                200,
                {
                    '1': resp.HistoryData(
                        {
                            "history": history_rotation1[HISTORY],
                            "signatures": {
                                "signer": rotation1_sign_sig,
                                "rotation": rotation1_rot_sig
                            }
                        }
                    ),
                    '0': resp.HistoryData(
                        {
                            "history": history_inception[HISTORY],
                            "signatures": {
                                "signer": inception_sig,
                            }
                        }
                    )
                }
            )

    }

    consense.validateData(data)

    exp_data = {
        '1': resp.HistoryData(
            {
                "history": history_rotation1[HISTORY],
                "signatures": {
                    "signer": rotation1_sign_sig,
                    "rotation": rotation1_rot_sig
                }
            }
        ),
        '0': resp.HistoryData(
            {
                "history": history_inception[HISTORY],
                "signatures": {
                    "signer": inception_sig,
                }
            }
        )
    }
    sha = sha256(str(ODict(exp_data)).encode()).hexdigest()

    assert consense.valid_data == {
        sha: {
            '1': {
                "history": history_rotation1[HISTORY],
                "signatures": {
                    "signer": rotation1_sign_sig,
                    "rotation": rotation1_rot_sig
                }
            },
            '0': {
                "history": history_inception[HISTORY],
                "signatures": {
                    "signer": inception_sig,
                }
            }
        }
    }
    assert sha in consense.valid_match_counts
    assert consense.valid_match_counts[sha] == 2


def testValidateDataValidSigsConflictingData():
    consense = consensing.CompositeConsense()
    history_inception = gen.historyGen()  # (history, vk1, sk1, vk2, sk2)
    url8000 = 'http://localhost:8000/event/{}'.format(history_inception[HISTORY]["id"])
    url8080 = 'http://localhost:8080/event/{}'.format(history_inception[HISTORY]["id"])
    url8081 = 'http://localhost:8081/event/{}'.format(history_inception[HISTORY]["id"])

    ppvk, ppsk, ppdid = gen.keyGen()
    history_rotation1 = deepcopy(history_inception)
    history_rotation1[HISTORY]["signers"].append(ppvk)
    history_rotation1[HISTORY]["signer"] = 1

    bHistory_inception = json.dumps(history_inception[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()
    bHistory_rotation = json.dumps(history_rotation1[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()
    inception_sig = signing.signResource(bHistory_inception, gen.key64uToKey(history_inception[SK1]))
    rotation1_sign_sig = signing.signResource(bHistory_rotation, gen.key64uToKey(history_inception[SK1]))
    rotation1_rot_sig = signing.signResource(bHistory_rotation, gen.key64uToKey(history_inception[SK2]))

    bad_history_inception = gen.historyGen()  # (history, vk1, sk1, vk2, sk2)
    bad_ppvk, bad_ppsk, bad_ppdid = gen.keyGen()
    bad_history_rotation1 = deepcopy(bad_history_inception)
    bad_history_rotation1[HISTORY]["signers"].append(bad_ppvk)
    bad_history_rotation1[HISTORY]["signer"] = 1

    bad_bHistory_inception = json.dumps(bad_history_inception[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()
    bad_bHistory_rotation = json.dumps(bad_history_rotation1[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()
    bad_inception_sig = signing.signResource(bad_bHistory_inception, gen.key64uToKey(bad_history_inception[SK1]))
    bad_rotation1_sign_sig = signing.signResource(bad_bHistory_rotation, gen.key64uToKey(bad_history_inception[SK1]))
    bad_rotation1_rot_sig = signing.signResource(bad_bHistory_rotation, gen.key64uToKey(bad_history_inception[SK2]))

    data = {
        url8000:
            resp.DideryResponse(
                url8000,
                200,
                {
                    '1': resp.HistoryData(
                        {
                            "history": history_rotation1[HISTORY],
                            "signatures": {
                                "signer": rotation1_sign_sig,
                                "rotation": rotation1_rot_sig
                            }
                        }
                    ),
                    '0': resp.HistoryData(
                        {
                            "history": history_inception[HISTORY],
                            "signatures": {
                                "signer": inception_sig,
                            }
                        }
                    )
                }
            ),
        url8080:
            resp.DideryResponse(
                url8080,
                200,
                {
                    '1': resp.HistoryData(
                        {
                            "history": bad_history_rotation1[HISTORY],
                            "signatures": {
                                "signer": bad_rotation1_sign_sig,
                                "rotation": bad_rotation1_rot_sig
                            }
                        }
                    ),
                    '0': resp.HistoryData(
                        {
                            "history": bad_history_inception[HISTORY],
                            "signatures": {
                                "signer": bad_inception_sig,
                            }
                        }
                    )
                }
            ),
        url8081:
            resp.DideryResponse(
                url8081,
                200,
                {
                    '1': resp.HistoryData(
                        {
                            "history": history_rotation1[HISTORY],
                            "signatures": {
                                "signer": rotation1_sign_sig,
                                "rotation": rotation1_rot_sig
                            }
                        }
                    ),
                    '0': resp.HistoryData(
                        {
                            "history": history_inception[HISTORY],
                            "signatures": {
                                "signer": inception_sig,
                            }
                        }
                    )
                }
            )

    }

    consense.validateData(data)

    exp_data = {
        '1': resp.HistoryData(
            {
                "history": history_rotation1[HISTORY],
                "signatures": {
                    "signer": rotation1_sign_sig,
                    "rotation": rotation1_rot_sig
                }
            }
        ),
        '0': resp.HistoryData(
            {
                "history": history_inception[HISTORY],
                "signatures": {
                    "signer": inception_sig,
                }
            }
        )
    }
    bad_exp_data = {
        '1': resp.HistoryData(
            {
                "history": bad_history_rotation1[HISTORY],
                "signatures": {
                    "signer": bad_rotation1_sign_sig,
                    "rotation": bad_rotation1_rot_sig
                }
            }
        ),
        '0': resp.HistoryData(
            {
                "history": bad_history_inception[HISTORY],
                "signatures": {
                    "signer": bad_inception_sig,
                }
            }
        )
    }
    sha = sha256(str(ODict(exp_data)).encode()).hexdigest()
    bad_sha = sha256(str(ODict(bad_exp_data)).encode()).hexdigest()

    assert consense.valid_data == {
        sha: {
            '1': {
                "history": history_rotation1[HISTORY],
                "signatures": {
                    "signer": rotation1_sign_sig,
                    "rotation": rotation1_rot_sig
                }
            },
            '0': {
                "history": history_inception[HISTORY],
                "signatures": {
                    "signer": inception_sig,
                }
            }
        },
        bad_sha: {
            '1': {
                "history": bad_history_rotation1[HISTORY],
                "signatures": {
                    "signer": bad_rotation1_sign_sig,
                    "rotation": bad_rotation1_rot_sig
                }
            },
            '0': {
                "history": bad_history_inception[HISTORY],
                "signatures": {
                    "signer": bad_inception_sig,
                }
            }
        }
    }
    assert sha in consense.valid_match_counts
    assert consense.valid_match_counts[sha] == 2
    assert bad_sha in consense.valid_match_counts
    assert consense.valid_match_counts[bad_sha] == 1


def testValidateDataIncompleteMajority():
    consense = consensing.CompositeConsense()
    history_inception = gen.historyGen()  # (history, vk1, sk1, vk2, sk2)
    url8000 = 'http://localhost:8000/event/{}'.format(history_inception[HISTORY]["id"])
    url8001 = 'http://localhost:8001/event/{}'.format(history_inception[HISTORY]["id"])
    url8080 = 'http://localhost:8080/event/{}'.format(history_inception[HISTORY]["id"])
    url8081 = 'http://localhost:8081/event/{}'.format(history_inception[HISTORY]["id"])

    ppvk, ppsk, ppdid = gen.keyGen()
    history_rotation1 = deepcopy(history_inception)
    history_rotation1[HISTORY]["signers"].append(ppvk)
    history_rotation1[HISTORY]["signer"] = 1

    bHistory_inception = json.dumps(history_inception[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()
    bHistory_rotation = json.dumps(history_rotation1[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()
    inception_sig = signing.signResource(bHistory_inception, gen.key64uToKey(history_inception[SK1]))
    rotation1_sign_sig = signing.signResource(bHistory_rotation, gen.key64uToKey(history_inception[SK1]))
    rotation1_rot_sig = signing.signResource(bHistory_rotation, gen.key64uToKey(history_inception[SK2]))

    bad_history_inception = gen.historyGen()  # (history, vk1, sk1, vk2, sk2)
    bad_ppvk, bad_ppsk, bad_ppdid = gen.keyGen()
    bad_history_rotation1 = deepcopy(bad_history_inception)
    bad_history_rotation1[HISTORY]["signers"].append(bad_ppvk)
    bad_history_rotation1[HISTORY]["signer"] = 1

    bad_bHistory_inception = json.dumps(bad_history_inception[HISTORY], ensure_ascii=False,
                                        separators=(',', ':')).encode()
    bad_bHistory_rotation = json.dumps(bad_history_rotation1[HISTORY], ensure_ascii=False,
                                       separators=(',', ':')).encode()
    bad_inception_sig = signing.signResource(bad_bHistory_inception, gen.key64uToKey(bad_history_inception[SK1]))
    bad_rotation1_sign_sig = signing.signResource(bad_bHistory_rotation, gen.key64uToKey(bad_history_inception[SK1]))
    bad_rotation1_rot_sig = signing.signResource(bad_bHistory_rotation, gen.key64uToKey(bad_history_inception[SK2]))

    data = {
        url8000:
            resp.DideryResponse(
                url8000,
                200,
                {
                    '1': resp.HistoryData(
                        {
                            "history": history_rotation1[HISTORY],
                            "signatures": {
                                "signer": rotation1_sign_sig,
                                "rotation": rotation1_rot_sig
                            }
                        }
                    ),
                    '0': resp.HistoryData(
                        {
                            "history": history_inception[HISTORY],
                            "signatures": {
                                "signer": inception_sig,
                            }
                        }
                    )
                }
            ),
        url8001:
            resp.DideryResponse(
                url8001,
                200,
                {
                    '1': resp.HistoryData(
                        {
                            "history": bad_history_rotation1[HISTORY],
                            "signatures": {
                                "signer": bad_rotation1_sign_sig,
                                "rotation": bad_rotation1_rot_sig
                            }
                        }
                    ),
                    '0': resp.HistoryData(
                        {
                            "history": bad_history_inception[HISTORY],
                            "signatures": {
                                "signer": bad_inception_sig,
                            }
                        }
                    )
                }
            ),
        url8080:
            resp.DideryResponse(
                url8080,
                200,
                {
                    '1': resp.HistoryData(
                        {
                            "history": bad_history_rotation1[HISTORY],
                            "signatures": {
                                "signer": bad_rotation1_sign_sig,
                                "rotation": bad_rotation1_rot_sig
                            }
                        }
                    ),
                    '0': resp.HistoryData(
                        {
                            "history": bad_history_inception[HISTORY],
                            "signatures": {
                                "signer": bad_inception_sig,
                            }
                        }
                    )
                }
            ),
        url8081:
            resp.DideryResponse(
                url8081,
                200,
                {
                    '1': resp.HistoryData(
                        {
                            "history": history_rotation1[HISTORY],
                            "signatures": {
                                "signer": rotation1_sign_sig,
                                "rotation": rotation1_rot_sig
                            }
                        }
                    ),
                    '0': resp.HistoryData(
                        {
                            "history": history_inception[HISTORY],
                            "signatures": {
                                "signer": inception_sig,
                            }
                        }
                    )
                }
            )

    }

    consense.validateData(data)

    exp_data = {
        '1': resp.HistoryData(
            {
                "history": history_rotation1[HISTORY],
                "signatures": {
                    "signer": rotation1_sign_sig,
                    "rotation": rotation1_rot_sig
                }
            }
        ),
        '0': resp.HistoryData(
            {
                "history": history_inception[HISTORY],
                "signatures": {
                    "signer": inception_sig,
                }
            }
        )
    }
    bad_exp_data = {
        '1': resp.HistoryData(
            {
                "history": bad_history_rotation1[HISTORY],
                "signatures": {
                    "signer": bad_rotation1_sign_sig,
                    "rotation": bad_rotation1_rot_sig
                }
            }
        ),
        '0': resp.HistoryData(
            {
                "history": bad_history_inception[HISTORY],
                "signatures": {
                    "signer": bad_inception_sig,
                }
            }
        )
    }
    sha = sha256(str(ODict(exp_data)).encode()).hexdigest()
    bad_sha = sha256(str(ODict(bad_exp_data)).encode()).hexdigest()

    assert consense.valid_data == {
        sha: {
            '1': {
                "history": history_rotation1[HISTORY],
                "signatures": {
                    "signer": rotation1_sign_sig,
                    "rotation": rotation1_rot_sig
                }
            },
            '0': {
                "history": history_inception[HISTORY],
                "signatures": {
                    "signer": inception_sig,
                }
            }
        },
        bad_sha: {
            '1': {
                "history": bad_history_rotation1[HISTORY],
                "signatures": {
                    "signer": bad_rotation1_sign_sig,
                    "rotation": bad_rotation1_rot_sig
                }
            },
            '0': {
                "history": bad_history_inception[HISTORY],
                "signatures": {
                    "signer": bad_inception_sig,
                }
            }
        }
    }
    assert sha in consense.valid_match_counts
    assert consense.valid_match_counts[sha] == 2
    assert bad_sha in consense.valid_match_counts
    assert consense.valid_match_counts[bad_sha] == 2


def testValidateDataWithHTTPError():
    consense = consensing.CompositeConsense()
    history_inception = gen.historyGen()  # (history, vk1, sk1, vk2, sk2)
    url8000 = 'http://localhost:8000/event/{}'.format(history_inception[HISTORY]["id"])
    url8080 = 'http://localhost:8080/event/{}'.format(history_inception[HISTORY]["id"])

    ppvk, ppsk, ppdid = gen.keyGen()
    history_rotation1 = deepcopy(history_inception)
    history_rotation1[HISTORY]["signers"].append(ppvk)
    history_rotation1[HISTORY]["signer"] = 1

    bHistory_inception = json.dumps(history_inception[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()
    bHistory_rotation = json.dumps(history_rotation1[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()
    inception_sig = signing.signResource(bHistory_inception, gen.key64uToKey(history_inception[SK1]))
    rotation1_sign_sig = signing.signResource(bHistory_rotation, gen.key64uToKey(history_inception[SK1]))
    rotation1_rot_sig = signing.signResource(bHistory_rotation, gen.key64uToKey(history_inception[SK2]))

    data = {
        url8000:
            resp.DideryResponse(
                url8000,
                200,
                {
                    '1': resp.HistoryData(
                        {
                            "history": history_rotation1[HISTORY],
                            "signatures": {
                                "signer": rotation1_sign_sig,
                                "rotation": rotation1_rot_sig
                            }
                        }
                    ),
                    '0': resp.HistoryData(
                        {
                            "history": history_inception[HISTORY],
                            "signatures": {
                                "signer": inception_sig,
                            }
                        }
                    )
                }
            ),
        url8080:
            resp.DideryResponse(
                url8080,
                400,
                {}
            )

    }

    consense.validateData(data)

    exp_data = {
        '1': resp.HistoryData(
            {
                "history": history_rotation1[HISTORY],
                "signatures": {
                    "signer": rotation1_sign_sig,
                    "rotation": rotation1_rot_sig
                }
            }
        ),
        '0': resp.HistoryData(
            {
                "history": history_inception[HISTORY],
                "signatures": {
                    "signer": inception_sig,
                }
            }
        )
    }
    sha = sha256(str(ODict(exp_data)).encode()).hexdigest()

    assert consense.valid_data == {
        sha: {
            '1': {
                "history": history_rotation1[HISTORY],
                "signatures": {
                    "signer": rotation1_sign_sig,
                    "rotation": rotation1_rot_sig
                }
            },
            '0': {
                "history": history_inception[HISTORY],
                "signatures": {
                    "signer": inception_sig,
                }
            }
        }
    }
    assert consense.valid_match_counts == {
        sha: 1
    }


def testValidateDataWithTimeOut():
    consense = consensing.CompositeConsense()
    history_inception = gen.historyGen()  # (history, vk1, sk1, vk2, sk2)
    url8000 = 'http://localhost:8000/event/{}'.format(history_inception[HISTORY]["id"])
    url8080 = 'http://localhost:8080/event/{}'.format(history_inception[HISTORY]["id"])

    ppvk, ppsk, ppdid = gen.keyGen()
    history_rotation1 = deepcopy(history_inception)
    history_rotation1[HISTORY]["signers"].append(ppvk)
    history_rotation1[HISTORY]["signer"] = 1

    bHistory_inception = json.dumps(history_inception[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()
    bHistory_rotation = json.dumps(history_rotation1[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()
    inception_sig = signing.signResource(bHistory_inception, gen.key64uToKey(history_inception[SK1]))
    rotation1_sign_sig = signing.signResource(bHistory_rotation, gen.key64uToKey(history_inception[SK1]))
    rotation1_rot_sig = signing.signResource(bHistory_rotation, gen.key64uToKey(history_inception[SK2]))

    data = {
        url8000:
            resp.DideryResponse(
                url8000,
                200,
                {
                    '1': resp.HistoryData(
                        {
                            "history": history_rotation1[HISTORY],
                            "signatures": {
                                "signer": rotation1_sign_sig,
                                "rotation": rotation1_rot_sig
                            }
                        }
                    ),
                    '0': resp.HistoryData(
                        {
                            "history": history_inception[HISTORY],
                            "signatures": {
                                "signer": inception_sig,
                            }
                        }
                    )
                }
            ),
        url8080:
            resp.DideryResponse(
                url8080,
                0,
                {}
            )

    }

    consense.validateData(data)

    exp_data = {
        '1': resp.HistoryData(
            {
                "history": history_rotation1[HISTORY],
                "signatures": {
                    "signer": rotation1_sign_sig,
                    "rotation": rotation1_rot_sig
                }
            }
        ),
        '0': resp.HistoryData(
            {
                "history": history_inception[HISTORY],
                "signatures": {
                    "signer": inception_sig,
                }
            }
        )
    }
    sha = sha256(str(ODict(exp_data)).encode()).hexdigest()

    assert consense.valid_data == {
        sha: {
            '1': {
                "history": history_rotation1[HISTORY],
                "signatures": {
                    "signer": rotation1_sign_sig,
                    "rotation": rotation1_rot_sig
                }
            },
            '0': {
                "history": history_inception[HISTORY],
                "signatures": {
                    "signer": inception_sig,
                }
            }
        }
    }
    assert consense.valid_match_counts == {
        sha: 1
    }
