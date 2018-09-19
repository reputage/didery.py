from .builder import SignableDataBuilder
from diderypy.models.responding import DideryResponse, HistoryData


class BasicHistoryBuilder(SignableDataBuilder):
    def __init__(self):
        SignableDataBuilder.__init__(self)

        self._ver_keys = [
            'u8TWIE28yAdu-lGrPHH2ZJ73GxoMBZx-D3cf6RMEaTc=',
            'u8TWIE28yAdu-lGrPHH2ZJ73GxoMBZx-D3cf6RMEaTc=',
            'unwAREZuniXEM_lPYX6BW4QZqmrO3C1mLVVlaaFQCMA=',
            'S62CjYF6I05P8erybWY92a8zvOBnVVXDciPWxdxsiA8='
        ]
        self._sign_keys = [
            'jWjzoCHRzcBijF4dvGc-4VMSx8u8DlRPekDbfSC6BgS7xNYgTbzIB276Uas8cfZknvcbGgwFnH4Pdx_pEwRpNw==',
            'jWjzoCHRzcBijF4dvGc-4VMSx8u8DlRPekDbfSC6BgS7xNYgTbzIB276Uas8cfZknvcbGgwFnH4Pdx_pEwRpNw==',
            'MyErIV4IZhhcX5W6QgXRFq7mxz2yti_kpFVVV80_dYu6fABERm6eJcQz-U9hfoFbhBmqas7cLWYtVWVpoVAIwA==',
            '2fiz_Zvcy602CsgOxbiejq7el-Kfpz9gSmEa6rjUxNxLrYKNgXojTk_x6vJtZj3ZrzO84GdVVcNyI9bF3GyIDw=='
        ]
        self._next_key_index = 2
        self.data = {
            'id': 'did:dad:u8TWIE28yAdu-lGrPHH2ZJ73GxoMBZx-D3cf6RMEaTc=',
            'signer': 0,
            'signers': [
                self._ver_keys[0],
                self._ver_keys[1]
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

    def withRotation(self):
        vk = self._ver_keys[self._next_key_index]
        self.data['signers'].append(vk)
        self.data['signer'] += 1
        # So that test data is deterministic the key index is modulod by the length of the self._ver_keys array
        self._next_key_index = (self._next_key_index + 1) % len(self._ver_keys)

        return self

    def withEmptyData(self):
        self.data = {}

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
            "signer": self._signData(self._sign_keys[0])
        }

    def withInvalidSignerSignature(self):
        self._signatures["signer"] = self._signData(self._invalid_sk)
        return self

    def withInvalidRotationSignature(self):
        self._signatures["rotation"] = self._signData(self._invalid_sk)
        return self

    def withRotation(self):
        BasicHistoryBuilder.withRotation(self)

        # get index into self._sign_keys
        signer_index = (self.data['signer'] - 1) % len(self._ver_keys)
        rotation_index = self.data['signer'] % len(self._ver_keys)

        self._signatures["signer"] = self._signData(self._sign_keys[signer_index])
        self._signatures["rotation"] = self._signData(self._sign_keys[rotation_index])

        return self

    def build(self):
        return HistoryData(
            {
                "history": self.data,
                "signatures": self._signatures
            }
        )

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


class CompositeHistoryBuilder(SignableDataBuilder):
    def __init__(self):
        SignableDataBuilder.__init__(self)
        self.data = [
            SignedHistoryBuilder()
        ]

    def withInvalidInceptionSig(self):
        self.data[0] = SignedHistoryBuilder().withInvalidSignerSignature()

        return self

    def withRotations(self, num_rotations=1):
        """
        function calculates how many rotations have already happened and
        then adds "num_rotations" more rotations before adding the data to the history
        :return: self
        """
        for i in range(0, num_rotations):
            history = SignedHistoryBuilder()

            for i in range(0, len(self.data)):
                history.withRotation()

            self.data.append(history)

        return self

    def withInvalidRotationSigAt(self, index):
        """
        sets the rotation signature to an invalid value for history rotation event at "index"
        :param index: which rotation should be invalidated
        :return: self
        """
        # Tests will fail gracefully if invalid index is supplied
        assert index < len(self.data)
        assert index >= 0

        self.data[index].withInvalidRotationSignature()

        return self

    def withEmptyData(self):
        self.data = []

        return self

    def build(self):
        composite = {}
        for key, value in enumerate(self.data):
            composite[str(key)] = value.build()

        return composite


class DideryResponseBuilder:
    def __init__(self, history):
        """
        Build a models.responding.DideryResponse object

        :param history: instance of SignableDataBuilder or subclass of it
        """
        self._url = "http://localhost:8080/history"
        self._status = 200
        self._history_builder = history
        self._history = history.build()

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
        return DideryResponse(self.url, self.status, self._history)

    @property
    def url(self):
        return self._url

    @property
    def status(self):
        return self._status

    @property
    def historyBuilder(self):
        return self._history_builder
