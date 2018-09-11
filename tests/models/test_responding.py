try:
    import simplejson as json
except ImportError:
    import json

from pydidery.help import signing
from pydidery.lib import generating as gen
from pydidery.models import responding as resp


HISTORY = 0
VK1 = 1
SK1 = 2
VK2 = 3
SK2 = 4


def testHistoryDataWithInceptionData():
    datum = gen.historyGen()
    bHistory = json.dumps(datum[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()
    signature = signing.signResource(bHistory, gen.key64uToKey(datum[SK1]))

    data = {
        "history": datum[HISTORY],
        "signatures": {
            "signer": signature
        }
    }

    history = resp.HistoryData(data)

    assert history.data == data
    assert history.bdata == json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode()
    assert history.body == data["history"]
    assert history.bbody == json.dumps(data["history"], ensure_ascii=False, separators=(",", ":")).encode()
    assert history.did == data["history"]["id"]
    assert history.vk == data["history"]["signers"][0]
    assert history.signer_sig == signature
    assert history.rotation_sig is None
    assert history.signature == signature
    assert history.valid is True


def testHistoryDataWithRotationData():
    datum = gen.historyGen()
    vk, sk, did = gen.keyGen()
    datum[HISTORY]["signer"] = 1
    datum[HISTORY]["signers"].append(vk)

    bHistory = json.dumps(datum[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()
    signer = signing.signResource(bHistory, gen.key64uToKey(datum[SK1]))
    rotation = signing.signResource(bHistory, gen.key64uToKey(datum[SK2]))

    data = {
        "history": datum[HISTORY],
        "signatures": {
            "signer": signer,
            "rotation": rotation
        }
    }

    history = resp.HistoryData(data)

    assert history.data == data
    assert history.bdata == json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode()
    assert history.body == data["history"]
    assert history.bbody == json.dumps(data["history"], ensure_ascii=False, separators=(",", ":")).encode()
    assert history.did == data["history"]["id"]
    assert history.vk == data["history"]["signers"][1]
    assert history.signer_sig == signer
    assert history.rotation_sig == rotation
    assert history.signature == rotation
    assert history.valid is True


def testHisoryDataWithInvalidSignature():
    datum = gen.historyGen()
    bHistory = json.dumps(datum[HISTORY], ensure_ascii=False, separators=(', ', ': ')).encode()

    # signed data has spaces that HistoryData object will not
    inv_signature = signing.signResource(bHistory, gen.key64uToKey(datum[SK1]))

    data = {
        "history": datum[HISTORY],
        "signatures": {
            "signer": inv_signature
        }
    }

    history = resp.HistoryData(data)

    assert history.valid is False


def testHisoryDataWithInvalidSignatures():
    datum = gen.historyGen()
    vk, sk, did = gen.keyGen()
    datum[HISTORY]["signer"] = 1
    datum[HISTORY]["signers"].append(vk)

    bHistory = json.dumps(datum[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()
    # signed data has spaces that HistoryData object will not
    bad_bHistory = json.dumps(datum[HISTORY], ensure_ascii=False, separators=(', ', ': ')).encode()
    signer = signing.signResource(bHistory, gen.key64uToKey(datum[SK1]))
    rotation = signing.signResource(bad_bHistory, gen.key64uToKey(datum[SK2]))

    data = {
        "history": datum[HISTORY],
        "signatures": {
            "signer": signer,
            "rotation": rotation
        }
    }

    history = resp.HistoryData(data)

    assert history.valid is False


def testOtpData():
    vk, sk, did = gen.keyGen()
    otp_data = {
        "id": did,
        "blob": "AeYbsHot0pmdWAcgTo5sD8iAuSQAfnH5U6wiIGpVNJQQoYKBYrPPxAoIc1i5SHCIDS8KFFgf8i0tDq8XGizaCgo9yju"
                "KHHNJZFi0QD9K6Vpt6fP0XgXlj8z_4D-7s3CcYmuoWAh6NVtYaf_GWw_2sCrHBAA2mAEsml3thLmu50Dw"
    }
    botp_data = json.dumps(otp_data, ensure_ascii=False, separators=(",", ":")).encode()
    signer = signing.signResource(botp_data, gen.key64uToKey(sk))

    data = {
        "otp_data": otp_data,
        "signatures": {
            "signer": signer
        }
    }

    otp = resp.OtpData(data)

    assert otp.data == data
    assert otp.bdata == json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode()
    assert otp.body == data["otp_data"]
    assert otp.bbody == json.dumps(data["otp_data"], ensure_ascii=False, separators=(",", ":")).encode()
    assert otp.did == did
    assert otp.vk == vk
    assert otp.signature == signer
    assert otp.valid is True


def testOtpDataWithInvalidSig():
    vk, sk, did = gen.keyGen()
    otp_data = {
        "id": did,
        "blob": "AeYbsHot0pmdWAcgTo5sD8iAuSQAfnH5U6wiIGpVNJQQoYKBYrPPxAoIc1i5SHCIDS8KFFgf8i0tDq8XGizaCgo9yju"
                "KHHNJZFi0QD9K6Vpt6fP0XgXlj8z_4D-7s3CcYmuoWAh6NVtYaf_GWw_2sCrHBAA2mAEsml3thLmu50Dw"
    }
    # signed data has spaces that OtpData object will not have
    botp_data = json.dumps(otp_data, ensure_ascii=False, separators=(", ", ": ")).encode()
    signer = signing.signResource(botp_data, gen.key64uToKey(sk))

    data = {
        "otp_data": otp_data,
        "signatures": {
            "signer": signer
        }
    }

    otp = resp.OtpData(data)

    assert otp.signature == signer
    assert otp.valid is False


def testDideryResponse():
    url = "http://localhost:8080"
    status = 200
    response = {
        "test": "data"
    }

    resp_obj = resp.DideryResponse(url, status, response)

    assert resp_obj.url == url
    assert resp_obj.status == status
    assert resp_obj.response == response


def testResponseFactoryWtihHistoryData():
    datum = gen.historyGen()
    bHistory = json.dumps(datum[HISTORY], ensure_ascii=False, separators=(',', ':')).encode()
    signature = signing.signResource(bHistory, gen.key64uToKey(datum[SK1]))

    data = {
        "history": datum[HISTORY],
        "signatures": {
            "signer": signature
        }
    }

    response = resp.responseFactory("", 200, data)

    assert type(response) == resp.DideryResponse
    assert type(response.response) == resp.HistoryData


def testResponseFactoryWtihOtpData():
    vk, sk, did = gen.keyGen()
    otp_data = {
        "id": did,
        "blob": "AeYbsHot0pmdWAcgTo5sD8iAuSQAfnH5U6wiIGpVNJQQoYKBYrPPxAoIc1i5SHCIDS8KFFgf8i0tDq8XGizaCgo9yju"
                "KHHNJZFi0QD9K6Vpt6fP0XgXlj8z_4D-7s3CcYmuoWAh6NVtYaf_GWw_2sCrHBAA2mAEsml3thLmu50Dw"
    }
    botp_data = json.dumps(otp_data, ensure_ascii=False, separators=(",", ":")).encode()
    signer = signing.signResource(botp_data, gen.key64uToKey(sk))

    data = {
        "otp_data": otp_data,
        "signatures": {
            "signer": signer
        }
    }

    response = resp.responseFactory("", 200, data)

    assert type(response) == resp.DideryResponse
    assert type(response.response) == resp.OtpData


def testResponseFactoryWtihBadData():
    data = {}

    response = resp.responseFactory("", 200, data)

    assert type(response) == resp.DideryResponse
    assert type(response.response) == resp.AbstractDideryData
