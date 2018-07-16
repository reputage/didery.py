try:
    import simplejson as json
except ImportError:
    import json

from .helping import verify64u, validateDid

MAJORITY = 2 / 3
RESPONSE = 0
STATUS = 1


class DideryData:
    """
        Base class for parsing didery request data for easier access
    """
    def __init__(self, data):
        self.bdata = b'{}'
        self.data = {}
        self.body = None
        self.signature = ""
        self.vk = ""
        self.did = ""


class HistoryData(DideryData):
    """
        Parse didery request data for easier access
    """
    def __init__(self, data):
        DideryData.__init__(self, data)

        self.bdata = json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode()
        self.data = data
        self.body = self.data["history"]
        self.vk = self.body["signers"][int(self.body["signer"])]
        self.did = self.body["id"]

        if "rotation" in self.data["signatures"]:
            self.signature = self.data["signatures"]["rotation"]
        else:
            self.signature = self.data["signatures"]["signer"]


class OtpData(DideryData):
    """
        Parse didery request data for easier access
    """
    def __init__(self, data):
        DideryData.__init__(self, data)

        self.bdata = json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode()
        self.data = data
        self.body = self.data["otp_data"]
        did, vk = validateDid(self.body["id"])
        self.signature = self.data["signatures"]["signer"]
        self.vk = vk
        self.did = did


def validateSignatures(data, dtype):
    """
        Validates signatures and data and then checks
        if a majority of the data items are equal by
        comparing their signatures.

        :param data: list of history dicts returned by the didery server
        :param dtype: string specifying to consense otp or history data
        :return: tuple if majority of signatures are valid else None
    """
    valid_data = {}
    sig_counts = {}
    num_valid = 0

    if not data:
        return None, None

    for url, datum in data.items():
        if datum[STATUS] != 200:
            continue

        if dtype == "history":
            datum = HistoryData(datum[RESPONSE])
        else:
            datum = OtpData(datum[RESPONSE])

        if verify64u(datum.signature, json.dumps(datum.body, ensure_ascii=False, separators=(',', ':')).encode(), datum.vk):
            num_valid += 1
            # keep track of data that belongs to signature
            valid_data[datum.signature] = datum.data
            # Count number of times the signature has been seen
            sig_counts[datum.signature] = sig_counts.get(datum.signature, 0) + 1

    # check that a majority of signatures are valid
    if len(data) * MAJORITY > num_valid:
        return None, None
    else:
        return valid_data, sig_counts


def consense(data, dtype="history"):
    """
        Validates signatures and data and then checks
        if a majority of the data items are equal by
        comparing their signatures.

        :param data: list of history dicts returned by the didery server
        :param dtype: string specifying to consense otp or history data
        :return: history dict if consensus is reached else None
    """

    valid_data, sig_counts = validateSignatures(data, dtype)

    # Not enough valid signatures
    if valid_data is None:
        return None

    # All signatures are equal
    if len(valid_data) == 1:
        return valid_data.popitem()[1]

    for sig, count in sig_counts.items():
        if count >= len(data) * MAJORITY:
            return valid_data[sig]

    return None
