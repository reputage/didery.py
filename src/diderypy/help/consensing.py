from hashlib import sha256

try:
    import simplejson as json
except ImportError:
    import json

from abc import ABC, abstractmethod
from collections import OrderedDict as ODict

from ..models.consensing import ConsensusResult


MAJORITY = 2 / 3


class AbstractConsense(ABC):
    def __init__(self):
        self.valid_data = {}
        self.valid_match_counts = {}
        self.num_valid = 0
        self.results = {}
        self.consensus = None

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

    def addMatchCount(self, hashd):
        self.valid_match_counts[hashd] = self.valid_match_counts.get(hashd, 0) + 1

    def addValidData(self, hashd, data):
        self.incrementValid()
        self.valid_data[hashd] = data

    def addSuccess(self, url, hashd, data, http_status):
        self.addResult(url, ConsensusResult.VALID, data, http_status)
        self.addMatchCount(hashd)
        self.addValidData(hashd, data)

    @abstractmethod
    def validateData(self, data):
        pass

    def consense(self, data):
        """
            Validates signatures and then checks
            if a majority of the data items are equal.

            :param data: list of history dicts returned by the didery server
            :return: tuple - history dict and dict of result strings for each url.
                     if consensus is not reached then None and the results dict are returned
        """
        if not data:
            raise ValueError("data cannot be None.")

        self.validateData(data)

        for hashData, count in self.valid_match_counts.items():
            if count >= len(data) * MAJORITY:
                self.consensus = self.valid_data[hashData]

        return self.consensus, self.results


class Consense(AbstractConsense):
    def __init__(self, valid_data=None, match_counts=None, results=None, num_valid=None):
        AbstractConsense.__init__(self)

        if valid_data:
            self.valid_data = valid_data

        if match_counts:
            self.valid_match_counts = match_counts

        if results:
            self.results = results

        if num_valid:
            self.num_valid = num_valid

    def validateData(self, data):
        """
            Checks for request errors and counts valid signatures

            :param data: dict of DideryResponse obj
        """
        for url, response in data.items():
            status = response.status
            data = response.response

            if status == 0:
                self.addTimeOut(url)  # Request timed out
                continue
            elif status != 200:
                self.addError(url, data, status)  # Error with request
                continue

            if data.valid:
                self.addSuccess(url, data.signature, data.data, status)  # Signature validated
            else:
                self.addFailure(url, data.data, status)  # Signature validation failed


class CompositeConsense(AbstractConsense):
    def __init__(self):
        AbstractConsense.__init__(self)

    def _dataToDict(self, data):
        temp = {}
        for index, event in data.items():
            temp[index] = event.data

        return temp

    def validateData(self, history_events):
        """
            Checks for request errors and counts valid signatures

            :param history_events: dict of history rotation events returned by the didery server
        """
        for url, response in history_events.items():
            status = response.status
            data = response.response

            if status == 0:
                self.addTimeOut(url)  # Request timed out
                continue
            elif status != 200:
                self.addError(url, data, status)  # Error with request
                continue

            valid = True if len(data) > 0 else False

            for index, event in data.items():
                if not event.valid:
                    valid = False

            if valid:
                sha = sha256(str(ODict(data)).encode()).hexdigest()
                self.addSuccess(url, sha, self._dataToDict(data), status)  # Signature validated
            else:
                self.addFailure(url, data, status)  # Signature validation failed
