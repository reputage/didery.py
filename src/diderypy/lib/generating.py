import base64
import libnacl
import libnacl.base
import stat
import os

import diderypy.lib.didering as didering
from diderypy.help import helping as help

"""
This module provides various key generation and manipulation functions for use with the didery server.  
Keys are generated using the python libnacl library.
"""


def keyToKey64u(key):
    """
    keyToKey64u allows you to convert a key from a byte string to a base64 url-file safe string.

    :param key: 32 byte string
    :return: base64 url-file safe string
    """
    if key is None:
        return None

    return base64.urlsafe_b64encode(key).decode("utf-8")


def key64uToKey(key64u):
    """
    key64uToKey allows you to convert a base64 url-file safe key string to a byte string

    :param key64u: base64 ulr-file safe string
    :return: byte string
    """
    if key64u is None:
        return None

    return base64.urlsafe_b64decode(key64u.encode("utf-8"))


def keyGen(seed=None):
    """
    keyGen generates a url-file safe base64 public private key pair.
    If a seed is not provided libnacl's randombytes() function will
    be used to generate a seed.

    :param seed: The seed value used during key generation.
    :return: url-file safe base64 verifier/public key, signing/private key
    """
    if seed is None:
        seed = libnacl.randombytes(libnacl.crypto_sign_SEEDBYTES)

    vk, sk = libnacl.crypto_sign_seed_keypair(seed)

    did = didering.didGen(vk)

    return keyToKey64u(vk), keyToKey64u(sk), did


def historyGen(initial_key_pair_seed=None, rotation_key_pair_seed=None):
    """
    historyGen generates a new key history dictionary and returns the
    history along with all generated keys. If a seed is not provided
    libnacl's randombytes() function will be used to generate a seed.

    :param initial_key_pair_seed: The seed value used during key generation for the initial key pair.
    :param rotation_key_pair_seed: The seed value used during key generation for the pre-rotated key pair.
    :return: a history dictionary with an "id", "signer" and "signers" field,
             url-file safe base64 verifier/public key string,
             url-file safe base64 signing/private key,
             url-file safe base64 pre-rotated verifier/public key,
             url-file safe base64 pre-rotated signing/private key
    """
    vk, sk, did = keyGen(initial_key_pair_seed)
    pre_rotated_vk, pre_rotated_sk, did = keyGen(rotation_key_pair_seed)

    history = {
        "id": didering.didGen64(vk),
        "signer": 0,
        "signers": [
            vk,
            pre_rotated_vk
        ]
    }

    return history, vk, sk, pre_rotated_vk, pre_rotated_sk


class DidBox(libnacl.base.BaseKey):
    crypto_didbox_SKBYTES = 64
    crypto_didbox_VKBYTES = 32

    def __init__(self, seed=None, sk=None, vk=None, did=None):
        if (sk is None and vk) or (sk and vk is None):
            raise ValueError('Both private and public keys required')

        if did and sk is None and vk is None:
            raise ValueError('Keys required with did')

        if sk and len(sk) != DidBox.crypto_didbox_SKBYTES or vk and len(vk) != DidBox.crypto_didbox_VKBYTES:
            raise ValueError('Invalid key')

        if sk is None and vk is None and seed is None:
            seed = libnacl.randombytes(libnacl.crypto_sign_SEEDBYTES)

            vk, sk = libnacl.crypto_sign_seed_keypair(seed)

            did = didering.didGen(vk)

        if seed and sk is None and vk is None:
            vk, sk = libnacl.crypto_sign_seed_keypair(seed)

            did = didering.didGen(vk)

        if sk and vk and did is None:
            did = didering.didGen(vk)

        self.seed = seed
        self.sk = sk
        self.vk = vk
        self.did = did

    def base64_vk(self):
        return keyToKey64u(self.vk)

    def base64_sk(self):
        return keyToKey64u(self.sk)

    def base64_seed(self):
        return keyToKey64u(self.seed)

    def for_json64(self):
        """
        Return a dictionary of the secret values we need to store.
        """
        pre = {}
        sk = self.base64_sk()
        vk = self.base64_vk()
        seed = self.base64_seed()
        if sk:
            pre['priv'] = sk
        if vk:
            pre['verify'] = vk
        if seed:
            pre['seed'] = seed

        return pre

    def save64(self, path, serial='simplejson'):
        """
        Safely save keys with perms of 0400
        """
        pre = self.for_json64()

        if serial == 'msgpack':
            import msgpack
            packaged = msgpack.dumps(pre)
        elif serial == 'json':
            import json
            packaged = json.dumps(pre)
        elif serial == 'simplejson':
            try:
                import simplejson as json
            except ImportError:
                import json
            packaged = json.dumps(pre)
        else:
            raise ValueError("Serialization method not recognized.")

        perm_other = stat.S_IROTH | stat.S_IWOTH | stat.S_IXOTH
        perm_group = stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP

        cumask = os.umask(perm_other | perm_group)
        with open(path, 'w+') as fp_:
            fp_.write(packaged)
        os.umask(cumask)

    def open(self, path):
        """
        Safely read keys with perms of 0600
        """
        if not os.path.exists(path):
            raise FileNotFoundError("File does not exist")
        else:
            if (os.stat(path).st_mode & 0o777) != 0o600:
                raise PermissionError("Insecure key file permissions!")

            data = help.parseKeyFile(path)

            self.sk = data['priv']
            self.vk = data['verify']
            self.seed = data['seed']
            self.did = didering.didGen(self.vk)
