class ConsensusResult:
    TIMEOUT = 0
    VALID = 1
    ERROR = 2
    FAILED = 3

    """
    Store info about a request and the status of it's validation
    """
    def __init__(self, url, req_status, response=None, http_status=None):
        self.url = url
        self.req_status = req_status
        self.response = response
        self.http_status = http_status

    def __str__(self):
        if self.req_status == ConsensusResult.TIMEOUT:
            return "Request Timed Out"
        elif self.req_status == ConsensusResult.VALID:
            return "Signature Validation Succeeded"
        elif self.req_status == ConsensusResult.ERROR:
            return "Error Handling Request. HTTP_{}".format(self.http_status)
        elif self.req_status == ConsensusResult.FAILED:
            return "Signature Validation Failed"
