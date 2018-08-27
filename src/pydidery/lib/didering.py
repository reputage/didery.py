import base64


def didGen(vk, method="dad"):
    """
    didGen accepts an EdDSA (Ed25519) key in the form of a byte string and returns a DID.

    :param vk: 32 byte verifier/public key from EdDSA (Ed25519) key
    :param method: W3C did method string. Defaults to "dad".
    :return: W3C DID string
    """
    if vk is None:
        return None

    # convert verkey to jsonable unicode string of base64 url-file safe
    vk64u = base64.urlsafe_b64encode(vk).decode("utf-8")

    return "did:{0}:{1}".format(method, vk64u)


def didGen64(vk64u, method="dad"):
    """
    didGen accepts a url-file safe base64 key in the form of a string and returns a DID.

    :param vk64u: base64 url-file safe verifier/public key from EdDSA (Ed25519) key
    :param method: W3C did method string. Defaults to "dad".
    :return: W3C DID string
    """
    if vk64u is None:
        return None

    return "did:{0}:{1}".format(method, vk64u)


def validateDid(did, method="dad"):
    """
    Parses and returns did index keystr from signer key indexed did
    as tuple (did, index, keystr)
    raises ValueError if fails parsing
    """
    try:  # correct did format  pre:method:keystr
        pre, meth, keystr = did.split(":")
    except ValueError as ex:
        raise ValueError("Malformed DID value")

    if pre != "did" or meth != method:
        raise ValueError("Invalid DID value")

    return did, keystr
