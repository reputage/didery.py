import base64
import libnacl

"""
This module provides various key generation and manipulation functions for use with the didery server.  
Keys are generated using the python libnacl library.
"""


def didGen(vk, method="dad"):
    """
    didGen accepts an EdDSA (Ed25519) key in the form of a byte string and returns a DID.

    :param vk: 32 byte verifier/public key from EdDSA (Ed25519) key
    :param method: W3C did method string. Defaults to "dad".
    :return: W3C DID string
    """
    # convert verkey to jsonable unicode string of base64 url-file safe
    vk64u = keyToKey64u(vk)

    return "did:{0}:{1}".format(method, vk64u)


def didGen64(vk64u, method="dad"):
    """
    didGen accepts a url-file safe base64 key in the form of a string and returns a DID.

    :param vk64u: base64 url-file safe verifier/public key from EdDSA (Ed25519) key
    :param method: W3C did method string. Defaults to "dad".
    :return: W3C DID string
    """
    return "did:{0}:{1}".format(method, vk64u)


def keyToKey64u(key):
    """
    keyToKey64u allows you to convert a key from a byte string to a base64 url-file safe string.

    :param key: 32 byte string
    :return: base64 url-file safe string
    """
    return base64.urlsafe_b64encode(key).decode("utf-8")


def key64uToKey(key64u):
    """
    key64uToKey allows you to convert a base64 url-file safe key string to a byte string

    :param key64u: base64 ulr-file safe string
    :return: byte string
    """
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

    return keyToKey64u(vk), keyToKey64u(sk)


def signResource(resource, sKey):
    """
    signResource accepts a byte string and an EdDSA (Ed25519) key in the form of a byte string
    and returns a base64 url-file safe signature.

    :param resource: byte string to be signed
    :param sKey: signing/private key from EdDSA (Ed25519) key
    :return: url-file safe base64 signature string
    """
    sig = libnacl.crypto_sign(resource, sKey)
    sig = sig[:libnacl.crypto_sign_BYTES]

    return keyToKey64u(sig)


def historyGen(seed=None):
    """
    historyGen generates a new key history dictionary and returns the
    history along with all generated keys. If a seed is not provided
    libnacl's randombytes() function will be used to generate a seed.

    :param seed: The seed value used during key generation.
    :return: a history dictionary with an "id", "signer" and "signers" field,
             url-file safe base64 verifier/public key string,
             url-file safe base64 signing/private key,
             url-file safe base64 pre-rotated verifier/public key,
             url-file safe base64 pre-rotated signing/private key
    """
    vk, sk = keyGen(seed)
    pre_rotated_vk, pre_rotated_sk = keyGen(seed)

    history = {
        "id": didGen64(vk),
        "signer": 0,
        "signers": [
            vk,
            pre_rotated_vk
        ]
    }

    return history, vk, sk, pre_rotated_vk, pre_rotated_sk
