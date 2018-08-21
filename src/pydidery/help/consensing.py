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
        self.body = None,
        self.bbody = b'{}'
        self.signature = ""
        self.vk = ""
        self.did = ""
        self.valid = False


class HistoryData(DideryData):
    """
        Parse didery request data for easier access
    """
    def __init__(self, data):
        DideryData.__init__(self, data)

        self.bdata = json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode()
        self.data = data
        self.body = self.data["history"]
        self.bbody = json.dumps(self.body, ensure_ascii=False, separators=(",", ":")).encode()
        self.vk = self.body["signers"][int(self.body["signer"])]
        self.did = self.body["id"]

        if "rotation" in self.data["signatures"]:
            self.signature = self.data["signatures"]["rotation"]
        else:
            self.signature = self.data["signatures"]["signer"]

        self.valid = verify64u(self.signature, self.bbody, self.vk)


class OtpData(DideryData):
    """
        Parse didery request data for easier access
    """
    def __init__(self, data):
        DideryData.__init__(self, data)

        self.bdata = json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode()
        self.data = data
        self.body = self.data["otp_data"]
        self.bbody = json.dumps(self.body, ensure_ascii=False, separators=(",", ":")).encode()
        did, vk = validateDid(self.body["id"])
        self.signature = self.data["signatures"]["signer"]
        self.vk = vk
        self.did = did

        self.valid = verify64u(self.signature, self.bbody, self.vk)


class ConsensusResult:
    TIMEOUT = 0
    SUCCESS = 1
    ERROR = 2
    FAILED = 3

    """
    Store info about a request and it's result
    """
    def __init__(self, url, req_status, response=None, http_status=None):
        self.url = url
        self.req_status = req_status
        self.response = response
        self.http_status = http_status

    def description(self):
        if self.req_status == ConsensusResult.TIMEOUT:
            return "Request Timed Out"
        elif self.req_status == ConsensusResult.SUCCESS:
            return "Request Succeeded"
        elif self.req_status == ConsensusResult.ERROR:
            return "Error Handling Request. HTTP_{}".format(self.http_status)
        elif self.req_status == ConsensusResult.FAILED:
            return "Signature Validation Failed"


class ConsensusResults:
    def __init__(self, valid_data=None, sig_counts=None, results=None, num_valid=None):
        self.valid_data = {}
        self.sig_counts = {}
        self.results = {}
        self.num_valid = 0
        self.consensus = None

        if valid_data:
            self.valid_data = valid_data

        if sig_counts:
            self.sig_counts = sig_counts

        if results:
            self.results = results

        if num_valid:
            self.num_valid = num_valid

    def incrementValid(self):
        self.num_valid += 1

    def addResult(self, url, req_status, response=None, http_status=None):
        self.results[url] = ConsensusResult(url, req_status, response, http_status)

    def addTimeOut(self, url):
        self.addResult(url, ConsensusResult.TIMEOUT)

    def addError(self, url, response, http_status):
        self.addResult(url, ConsensusResult.ERROR, response, http_status)

    def addFailure(self, url, response, http_status):
        self.addResult(url, ConsensusResult.FAILED, response, http_status)

    def addSigCount(self, signature):
        self.sig_counts[signature] = self.sig_counts.get(signature, 0) + 1

    def addValidData(self, signature, data):
        self.valid_data[signature] = data

    def updateValidData(self, url, signature, data, http_status):
        self.incrementValid()
        self.addResult(url, ConsensusResult.SUCCESS, data, http_status)
        self.addSigCount(signature)
        self.addValidData(signature, data)


def validateSignatures(data, dtype):
    """
        Validates signatures and data and then checks
        if a majority of the data items are equal by
        comparing their signatures.

        :param data: list of history dicts returned by the didery server
        :param dtype: string specifying to consense otp or history data
        :return: tuple if majority of signatures are valid else None
    """
    validationResults = ConsensusResults()

    for url, datum in data.items():
        response = datum[RESPONSE]
        status = datum[STATUS]

        if status == 0:
            validationResults.addTimeOut(url)  # Request timed out
            continue
        elif status != 200:
            validationResults.addError(url, response, status)  # Error with request
            continue

        if dtype == "history":
            datum = HistoryData(response)
        else:
            datum = OtpData(response)

        if datum.valid:
            validationResults.updateValidData(url, datum.signature, datum.data, status)  # Signature validated
        else:
            validationResults.addFailure(url, datum.data, status)  # Signature validation failed

    return validationResults


def consense(data, dtype="history"):
    """
        Validates signatures and data and then checks
        if a majority of the data items are equal by
        comparing their signatures.

        :param data: list of history dicts returned by the didery server
        :param dtype: string specifying to consense otp or history data
        :return: tuple - history dict and dict of result strings for each url.
                 if consensus is not reached then None and the results dict are returned
    """
    if not data:
        raise ValueError("data cannot be None.")

    results = validateSignatures(data, dtype)

    for sig, count in results.sig_counts.items():
        if count >= len(data) * MAJORITY:
            results.consensus = results.valid_data[sig]

    return results.consensus, results.results
