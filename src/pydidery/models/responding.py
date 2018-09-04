try:
    import simplejson as json
except ImportError:
    import json

from collections import OrderedDict as ODict

from ..lib.didering import validateDid
from ..help.signing import verify64u


def responseFactory(url, status, data):
    if "history" in data or ("deleted" in data and "history" in data["deleted"]):
        response = HistoryData(data)
    elif "otp_data" in data or ("deleted" in data and "otp_data" in data["deleted"]):
        response = OtpData(data)
    elif status == 200 and "event" in data[0]:
        response = {}
        for datum in data:
            key = str(datum["event"]["signer"])
            event = {
                "history": datum["event"],
                "signatures": datum["signatures"]
            }
            response[key] = HistoryData(event)
    else:
        response = DideryData(data)

    return DideryResponse(url, status, response)


class DideryResponse:
    def __init__(self, url, status, response):
        self.url = url
        self.status = status
        self.response = response

    def __str__(self):
        return str(ODict(self.__dict__)).replace("OrderedDict", "")

    def __repr__(self):
        return str(ODict(self.__dict__)).replace("OrderedDict", "DideryResponse")


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

    def __eq__(self, other):
        return self.data == other.data


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

    def __str__(self):
        return str(ODict(self.body)).replace("OrderedDict", "")

    def __repr__(self):
        return str(ODict(self.body)).replace("OrderedDict", "HistoryData")


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
