import arrow

try:
    import simplejson as json
except ImportError:
    import json

from ioflo.aio.http import Valet

# import didery.routing

from pydidery.lib import generating as gen
from pydidery.lib import otping as otp

vk, sk = gen.keyGen()
did = gen.didGen64(vk)
otpData = {
    "id": did,
    "blob": "AeYbsHot0pmdWAcgTo5sD8iAuSQAfnH5U6wiIGpVNJQQoYKBYrPPxAoIc1i5SHCIDS8KFFgf8i0tDq8XGizaCgo9yjuKHHNJZFi0QD9K"
            "6Vpt6fP0XgXlj8z_4D-7s3CcYmuoWAh6NVtYaf_GWw_2sCrHBAA2mAEsml3thLmu50Dw"
}

url1, url2 = "http://localhost:8080", "http://localhost:8000"
urls = ["http://localhost:8080", "http://localhost:8000"]


def testPostOtpBlob():
    result = otp.postOtpBlob(otpData, sk, urls)

    assert result[url1]["http_status"] == 201
    assert result[url2]["http_status"] == 201


def testGetOtpBlob():
    data, result = otp.getOtpBlob(did, urls)

    assert data['otp_data'] == otpData


def testPutOtpBlob():
    result = otp.putOtpBlob(otpData, sk, urls)

    assert result[url1]["http_status"] == 200
    assert result[url1]["data"]["otp_data"] == otpData
    assert result[url2]["http_status"] == 200
    assert result[url2]["data"]["otp_data"] == otpData


def testRemoveOtpBlob():
    result = otp.removeOtpBlob(did, sk, urls)

    assert result[url1]["http_status"] == 200
    assert result[url1]["data"]["deleted"]["otp_data"] == otpData
    assert result[url2]["http_status"] == 200
    assert result[url2]["data"]["deleted"]["otp_data"] == otpData
