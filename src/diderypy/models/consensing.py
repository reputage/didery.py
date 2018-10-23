from urllib.parse import urlparse


class ConsensusResult:
    """
    ConsensusResult object a container class for storing info about a request
    and the status of a requests validation during the consensing step.
    A list or dict of ConsensusResult objects will be returned by any function
    running didery.py's consensing algorithm.
    """
    TIMEOUT = 0
    VALID = 1
    ERROR = 2
    FAILED = 3

    def __init__(self, url, validation_status, response=None, http_status=None):
        """
        Initialize a ConsensusResult object

        Args:
            :param url: string, url that was queried
            :param validation_status: int, 0-3
            :param response: dict or model, containing response data from the above url
            :param http_status: int, the http response status from the request
        """
        self.url = url
        if 0 > validation_status > 3:
            raise ValueError("validation_status must be between 0 and 3")
        self.validation_status = validation_status
        self.response = response
        self.http_status = http_status

    def __str__(self):
        url = urlparse(self.url)
        str_rep = "{}://{}: ".format(url.scheme, url.netloc).ljust(34)

        if self.validation_status == ConsensusResult.TIMEOUT:
            str_rep += "Request Timed Out"
        elif self.validation_status == ConsensusResult.VALID:
            str_rep += "Signature Validation Succeeded"
        elif self.validation_status == ConsensusResult.ERROR:
            str_rep += "Error Handling Request. HTTP_{}".format(self.http_status)
        elif self.validation_status == ConsensusResult.FAILED:
            str_rep += "Signature Validation Failed"

        return str_rep

    def __repr__(self):
        url = urlparse(self.url)
        str_rep = "{}://{}:\t".format(url.scheme, url.netloc)

        if self.validation_status == ConsensusResult.TIMEOUT:
            str_rep += "Request Timed Out.\t"
        elif self.validation_status == ConsensusResult.VALID:
            str_rep += "Signature Validation Succeeded.\t"
        elif self.validation_status == ConsensusResult.ERROR:
            str_rep += "Error Handling Request.\t"
        elif self.validation_status == ConsensusResult.FAILED:
            str_rep += "Signature Validation Failed.\t"

        str_rep += "HTTP_{}".format(self.http_status)

        return str_rep
