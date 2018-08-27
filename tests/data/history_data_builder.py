from .builder import DataBuilder
from pydidery.models.responding import DideryResponse, HistoryData


class BasicHistoryBuilder(DataBuilder):
    def __init__(self):
        DataBuilder.__init__(self)

        self._vk = 'u8TWIE28yAdu-lGrPHH2ZJ73GxoMBZx-D3cf6RMEaTc='
        self._sk = 'jWjzoCHRzcBijF4dvGc-4VMSx8u8DlRPekDbfSC6BgS7xNYgTbzIB276Uas8cfZknvcbGgwFnH4Pdx_pEwRpNw=='
        self._pvk = 'u8TWIE28yAdu-lGrPHH2ZJ73GxoMBZx-D3cf6RMEaTc='
        self._psk = 'jWjzoCHRzcBijF4dvGc-4VMSx8u8DlRPekDbfSC6BgS7xNYgTbzIB276Uas8cfZknvcbGgwFnH4Pdx_pEwRpNw=='
        self._ppvk = 'unwAREZuniXEM_lPYX6BW4QZqmrO3C1mLVVlaaFQCMA='
        self._ppsk = 'MyErIV4IZhhcX5W6QgXRFq7mxz2yti_kpFVVV80_dYu6fABERm6eJcQz-U9hfoFbhBmqas7cLWYtVWVpoVAIwA=='
        self._pppvk = 'S62CjYF6I05P8erybWY92a8zvOBnVVXDciPWxdxsiA8='
        self._pppsk = '2fiz_Zvcy602CsgOxbiejq7el-Kfpz9gSmEa6rjUxNxLrYKNgXojTk_x6vJtZj3ZrzO84GdVVcNyI9bF3GyIDw=='
        self.data = {
            'id': 'did:dad:u8TWIE28yAdu-lGrPHH2ZJ73GxoMBZx-D3cf6RMEaTc=',
            'signer': 0,
            'signers': [
                self._vk,
                self._pvk
            ]
        }

    def withId(self, did):
        self.data["id"] = did
        return self

    def withSigner(self, signer):
        self.data["signer"] = signer
        return self

    def withSigners(self, signers):
        self.data["signers"] = signers
        return self

    def withAdditionToSigners(self, vk):
        self.data["signers"].append(vk)
        return self

    @property
    def history(self):
        return self.data


class SignedHistoryBuilder(BasicHistoryBuilder):
    def __init__(self):
        BasicHistoryBuilder.__init__(self)

        self._invalid_vk = 'LdXz8KxuGr9bpO9voCRAxUAWuS5z3hVie31HmZj7lE0=',
        self._invalid_sk = 'oybqsj-N4sTVZaST-plc0W4AIVcMOhqXIjlvXSimQ1ct1fPwrG4av1uk72-gJEDFQBa5LnPeFWJ7fUeZmPuUTQ=='

        self._signatures = {
            "signer": self._signData(self._sk)
        }

    def withInvalidSignerSignature(self):
        self._signatures["signer"] = self._signData(self._invalid_sk)
        return self

    def withInvalidRotationSignature(self):
        self._signatures["rotation"] = self._signData(self._invalid_sk)
        return self

    def build(self):
        return {
            "history": self.data,
            "signatures": self._signatures
        }

    @property
    def signatures(self):
        return self._signatures

    @property
    def signerSig(self):
        return self._signatures["signer"]

    @property
    def rotationSig(self):
        if "rotation" in self._signatures:
            return self._signatures["rotation"]
        else:
            return None


class DideryResponseBuilder:
    def __init__(self, history):
        self._url = "http://localhost:8080/history"
        self._status = 200
        self._history = history

    def withStatus(self, http_status):
        self._status = http_status
        return self

    def withUrl(self, url):
        self._url = url
        return self

    def withPort(self, port):
        self._url = "http://localhost:{}/history".format(port)
        return self

    def build(self):
        return DideryResponse(self.url, self.status, HistoryData(self.history.build()))

    @property
    def url(self):
        return self._url

    @property
    def status(self):
        return self._status

    @property
    def history(self):
        return self._history
