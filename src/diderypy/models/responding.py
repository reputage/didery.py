try:
    import simplejson as json
except ImportError:
    import json

from collections import OrderedDict as ODict

from ..lib.didering import validateDid
from ..help.signing import verify64u


def responseFactory(url, status, data):
    """
    responseFactory()  implements the factory pattern to build objects for
    history, otp, and events data based on the format of the data that is passed to it

    :param url: url string that was queried
    :param status: integer representing the http response status from the request
    :param data: dict containing response data from the above url

    :return: DideryResponse object containing in it's response field either a
             HistoryData object, OtpData object, or a dict of HistoryData objects
             depending on if you passed rotation history data, otp encrypted blob data, or events data.
    """
    if data:
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
            response = AbstractDideryData(data)
    else:
        response = AbstractDideryData(data)

    return DideryResponse(url, status, response)


class DideryResponse:
    """
    DideryResponse object is a container class for storing info about a HTTP response.
    """
    def __init__(self, url, status, response):
        """

        :param url: url string that was queried
        :param status: integer representing the http response status from the request
        :param response: dict or model containing response data from the above url
        """
        self.url = url
        self.status = status
        self.response = response

    def __str__(self):
        return str(ODict(self.__dict__)).replace("OrderedDict", "")

    def __repr__(self):
        return str(ODict(self.__dict__)).replace("OrderedDict", "DideryResponse")


class AbstractDideryData:
    """
        AbstractDideryData object is an abstract parent class for storing response data from didery servers.
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


class HistoryData(AbstractDideryData):
    """
        HistoryData is a container class that implements the AbstractDideryData class.
        It adds three additional attributes to the base class.
    """

    def __init__(self, data):
        """

        :param data: dict returned from request to /history/ endpoint on didery servers
        """
        AbstractDideryData.__init__(self, data)

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
    def previous_vk(self):
        signer = int(self.body["signer"])
        if signer == 0:
            return None

        return self.body["signers"][signer-1]

    @property
    def signer_sig(self):
        return self._data["signatures"]["signer"]

    @property
    def rotation_sig(self):
        if "rotation" in self._data["signatures"]:
            return self._data["signatures"]["rotation"]
        else:
            return None

    @property
    def signature(self):
        if self.rotation_sig:
            return self.rotation_sig
        else:
            return self.signer_sig

    @property
    def valid(self):
        if self.rotation_sig:
            rotation = verify64u(self.rotation_sig, self.bbody, self.vk)
            signer = verify64u(self.signer_sig, self.bbody, self.previous_vk)
        else:
            rotation = True
            signer = verify64u(self.signer_sig, self.bbody, self.vk)

        return signer and rotation

    def __str__(self):
        return str(ODict(self.body)).replace("OrderedDict", "")

    def __repr__(self):
        return str(ODict(self.body)).replace("OrderedDict", "HistoryData")


class OtpData(AbstractDideryData):
    """
        OtpData is a container class that implements the AbstractDideryData class.
        It does not currently add any additional attributes or methods to the base class.
    """

    def __init__(self, data):
        """

        :param data: dict returned from request to /blob/ endpoint on didery servers
        """
        AbstractDideryData.__init__(self, data)

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
