import pytest

try:
    import simplejson as json
except ImportError:
    import json

from ioflo.aio.http import Valet

# import didery.routing

from pydidery.lib import generating as gen
from pydidery.lib import otping as otp

vk, sk, did = gen.keyGen()
otpData = {
    "id": did,
    "blob": "AeYbsHot0pmdWAcgTo5sD8iAuSQAfnH5U6wiIGpVNJQQoYKBYrPPxAoIc1i5SHCIDS8KFFgf8i0tDq8XGizaCgo9yjuKHHNJZFi0QD9K"
            "6Vpt6fP0XgXlj8z_4D-7s3CcYmuoWAh6NVtYaf_GWw_2sCrHBAA2mAEsml3thLmu50Dw"
}

url1, url2 = "http://localhost:8080/blob", "http://localhost:8000/blob"
urls = ["http://localhost:8080", "http://localhost:8000"]


def testPostOtpBlob():
    result = otp.postOtpBlob(otpData, sk, urls)

    assert result[url1].status == 201
    assert result[url2].status == 201


def testPostOtpBlobNoUrls():
    with pytest.raises(ValueError) as ex:
        otp.postOtpBlob(otpData, sk, None)


def testPostOtpBlobEmptyUrls():
    with pytest.raises(ValueError) as ex:
        otp.postOtpBlob(otpData, sk, [])


def testPostOtpBlobNoSk():
    with pytest.raises(ValueError) as ex:
        otp.postOtpBlob(otpData, None, urls)


def testPostOtpBlobEmptySk():
    with pytest.raises(ValueError) as ex:
        otp.postOtpBlob(otpData, "", urls)


def testGetOtpBlob():
    data, result = otp.getOtpBlob(did, urls)

    assert data['otp_data'] == otpData


def testGetOtpBlobNoUrls():
    with pytest.raises(ValueError) as ex:
        otp.getOtpBlob(did, None)


def testGetOtpBlobEmptyUrls():
    with pytest.raises(ValueError) as ex:
        otp.getOtpBlob(did, [])


def testPutOtpBlob():
    result = otp.putOtpBlob(otpData, sk, urls)

    assert result[url1+"/"+otpData["id"]].status == 200
    assert result[url1+"/"+otpData["id"]].response.body == otpData
    assert result[url2+"/"+otpData["id"]].status == 200
    assert result[url2+"/"+otpData["id"]].response.body == otpData


def testPutOtpBlobNoUrls():
    with pytest.raises(ValueError) as ex:
        otp.putOtpBlob(otpData, sk, None)


def testPutOtpBlobEmptyUrls():
    with pytest.raises(ValueError) as ex:
        otp.putOtpBlob(otpData, sk, [])


def testPutOtpBlobNoSk():
    with pytest.raises(ValueError) as ex:
        otp.putOtpBlob(otpData, None, urls)


def testPutOtpBlobEmptySk():
    with pytest.raises(ValueError) as ex:
        otp.putOtpBlob(otpData, "", urls)


def testRemoveOtpBlob():
    result = otp.removeOtpBlob(did, sk, urls)

    assert result[url1+"/"+did].status == 200
    assert result[url1+"/"+did].response.body == otpData
    assert result[url2+"/"+did].status == 200
    assert result[url2+"/"+did].response.body == otpData


def testRemoveOtpBlobNoUrls():
    with pytest.raises(ValueError) as ex:
        otp.removeOtpBlob(did, sk, None)


def testRemoveOtpBlobEmptyUrls():
    with pytest.raises(ValueError) as ex:
        otp.removeOtpBlob(did, sk, [])


def testRemoveOtpBlobNoSk():
    with pytest.raises(ValueError) as ex:
        otp.removeOtpBlob(did, None, urls)


def testRemoveOtpBlobEmptySk():
    with pytest.raises(ValueError) as ex:
        otp.removeOtpBlob(did, "", urls)
