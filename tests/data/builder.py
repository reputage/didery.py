import libnacl
import base64

try:
    import simplejson as json
except ImportError:
    import json


class DataBuilder:
    def __init__(self):
        self.data = None

    def build(self):
        return self.data

    def _signData(self, sk):
        bdata = json.dumps(self.data, ensure_ascii=False, separators=(",", ":")).encode()
        bsk = base64.urlsafe_b64decode(sk.encode("utf-8"))
        sig = libnacl.crypto_sign(bdata, bsk)
        sig = sig[:libnacl.crypto_sign_BYTES]

        return base64.urlsafe_b64encode(sig).decode("utf-8")
