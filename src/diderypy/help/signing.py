import libnacl

from ..lib import generating as gen


def signResource(resource, sKey):
    """
    signResource accepts a byte string and an EdDSA (Ed25519) key in the form of a byte string
    and returns a base64 url-file safe signature.

    :param resource: byte string to be signed
    :param sKey: signing/private key from EdDSA (Ed25519) key
    :return: url-file safe base64 signature string
    """
    if resource is None:
        return None

    sig = libnacl.crypto_sign(resource, sKey)
    sig = sig[:libnacl.crypto_sign_BYTES]

    return gen.keyToKey64u(sig)


def verify(sig, msg, vk):
    """
    Returns True if signature sig of message msg is verified with
    verification key vk Otherwise False
    All of sig, msg, vk are bytes
    """
    try:
        result = libnacl.crypto_sign_open(sig + msg, vk)
    except Exception as ex:
        return False
    return True if result else False


def verify64u(signature, message, verkey):
    """
    Returns True if signature is valid for message with respect to verification
    key verkey

    signature and verkey are encoded as unicode base64 url-file strings
    and message is unicode string as would be the case for a json object

    """
    sig = gen.key64uToKey(signature)
    vk = gen.key64uToKey(verkey)

    return verify(sig, message, vk)
