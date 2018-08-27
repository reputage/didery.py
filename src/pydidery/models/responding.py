try:
    import simplejson as json
except ImportError:
    import json

from ..lib.didering import validateDid
from ..help.signing import verify64u


def responseFactory(url, status, data):
    if "history" in url:
        response = HistoryData(data)
    elif "blob" in url:
        response = OtpData(data)
    else:
        response = DideryData(data)

    return DideryResponse(url, status, response)


class DideryResponse:
    def __init__(self, url, status, response):
        self.url = url
        self.status = status
        self.response = response


class DideryData:
    """
        Base class for parsing didery response data for easier access
    """

    def __init__(self, data):
        self._data = data

    @property
    def data(self):
        return self._data

    @property
    def bdata(self):
        return json.dumps(self._data, ensure_ascii=False, separators=(",", ":")).encode()

    @property
    def body(self):
        return None

    @property
    def bbody(self):
        return json.dumps(self.body, ensure_ascii=False, separators=(",", ":")).encode()

    @property
    def did(self):
        return self.body["id"]

    @property
    def vk(self):
        return None

    @property
    def signature(self):
        return None

    @property
    def valid(self):
        return verify64u(self.signature, self.bbody, self.vk)


class HistoryData(DideryData):
    """
        Parse didery rotation history response data for easier access
    """

    def __init__(self, data):
        DideryData.__init__(self, data)

    @property
    def body(self):
        if "deleted" in self._data:
            return self._data["deleted"]["history"]
        else:
            return self._data["history"]

    @property
    def vk(self):
        signer = int(self.body["signer"])
        return self.body["signers"][signer]

    @property
    def signature(self):
        if "rotation" in self._data["signatures"]:
            return self._data["signatures"]["rotation"]
        else:
            return self._data["signatures"]["signer"]


class OtpData(DideryData):
    """
        Parse didery otp blob response data for easier access
    """

    def __init__(self, data):
        DideryData.__init__(self, data)

    @property
    def body(self):
        if "deleted" in self._data:
            return self._data["deleted"]["otp_data"]
        else:
            return self._data["otp_data"]

    @property
    def vk(self):
        did, vk = validateDid(self.body["id"])
        return vk

    @property
    def signature(self):
        return self._data["signatures"]["signer"]
