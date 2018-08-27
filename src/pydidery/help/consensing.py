try:
    import simplejson as json
except ImportError:
    import json

from ..models.consensing import ConsensusResult


MAJORITY = 2 / 3


class Consense:
    def __init__(self, valid_data=None, sig_counts=None, results=None, num_valid=None):
        self.valid_data = {}
        self.valid_sig_counts = {}
        self.results = {}
        self.num_valid = 0
        self.consensus = None

        if valid_data:
            self.valid_data = valid_data

        if sig_counts:
            self.valid_sig_counts = sig_counts

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
        self.valid_sig_counts[signature] = self.valid_sig_counts.get(signature, 0) + 1

    def addValidData(self, signature, data):
        self.valid_data[signature] = data

    def updateValidData(self, url, signature, data, http_status):
        self.incrementValid()
        self.addResult(url, ConsensusResult.SUCCESS, data, http_status)
        self.addSigCount(signature)
        self.addValidData(signature, data)

    def validateData(self, data):
        """
            Validates signatures and data and then checks
            if a majority of the data items are equal by
            comparing their signatures.

            :param data: list of history dicts returned by the didery server
            :param dtype: string specifying to consense otp or history data
            :return: tuple if majority of signatures are valid else None
        """
        for url, response in data.items():
            status = response.status
            response = response.response

            if status == 0:
                self.addTimeOut(url)  # Request timed out
                continue
            elif status != 200:
                self.addError(url, response, status)  # Error with request
                continue

            if response.valid:
                self.updateValidData(url, response.signature, response.data, status)  # Signature validated
            else:
                self.addFailure(url, response.data, status)  # Signature validation failed

    def consense(self, data):
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

        self.validateData(data)

        for sig, count in self.valid_sig_counts.items():
            if count >= len(data) * MAJORITY:
                self.consensus = self.valid_data[sig]

        return self.consensus, self.results
