generating.py
=============

This module provides various key generation and manipulation functions
for use with the didery server. Keys are generated using the python
libnacl library.

generating.didGen(vk, [method])
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

didGen accepts an EdDSA (Ed25519) key in the form of a byte string and
returns a DID.

| **vk** (*required*)- 32 byte verifier/public key from EdDSA (Ed25519)
  key
| **method** (*optional*) - `W3C did
  method <https://w3c-ccg.github.io/did-spec/#specific-did-method-schemes>`__\ string.
  Defaults to "dad".

**returns** - `W3C DID <https://w3c-ccg.github.io/did-spec/>`__ string

Example
^^^^^^^

.. code:: python

    import pydidery.lib.generating as gen


    vk = b'\xfdv\xae\xeb\xe7\x08Q\xaf\xedY\xcf\x8b"\xfc\xa6\xeb\x1c@\x89}\xdb\xed\x16\xa5\xb6\x88\x18\xc8\x1a%O\x83'

    # use the default method
    did1 = gen.didGen(vk)

    # or you can specify a method like igo
    did2 = gen.didGen(vk, "igo")

    print(did1)
    print(did2)

Output
^^^^^^

::

    did:dad:_Xau6-cIUa_tWc-LIvym6xxAiX3b7RaltogYyBolT4M=
    did:igo:_Xau6-cIUa_tWc-LIvym6xxAiX3b7RaltogYyBolT4M=

generating.didGen64(vk64u, [method]):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

didGen accepts a url-file safe base64 key in the form of a string and
returns a DID.

| **vk64u** (*required*)- base64 url-file safe verifier/public key from
  EdDSA (Ed25519) key
| **method** (*optional*) - `W3C did
  method <https://w3c-ccg.github.io/did-spec/#specific-did-method-schemes>`__\ string.
  Defaults to "dad"

**returns** - `W3C DID <https://w3c-ccg.github.io/did-spec/>`__ string

Example
^^^^^^^

.. code:: python

    import pydidery.lib.generating as gen


    vk = "nxESHveBmK9RsEkgaZi-cNPvW0zO-ujOWEW7oKb7EYI="

    # use the default method
    did1 = gen.didGen64(vk)

    # or you can specify a method like igo
    did2 = gen.didGen64(vk, "igo")

    print(did1)
    print(did2)

Output
^^^^^^

::

    did:dad:nxESHveBmK9RsEkgaZi-cNPvW0zO-ujOWEW7oKb7EYI=
    did:igo:nxESHveBmK9RsEkgaZi-cNPvW0zO-ujOWEW7oKb7EYI=

generating.keyToKey64u(key):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

keyToKey64u allows you to convert a key from a byte string to a base64
url-file safe string.

**key** (*required*)- 32 byte string

**returns** - base64 url-file safe string

Example
^^^^^^^

.. code:: python

    import pydidery.lib.generating as gen


    vk = b'\xfdv\xae\xeb\xe7\x08Q\xaf\xedY\xcf\x8b"\xfc\xa6\xeb\x1c@\x89}\xdb\xed\x16\xa5\xb6\x88\x18\xc8\x1a%O\x83'

    # convert the key
    key = gen.keyToKey64u(vk)

    print(key)

Output
^^^^^^

::

    _Xau6-cIUa_tWc-LIvym6xxAiX3b7RaltogYyBolT4M=

generating.key64uToKey(key64u):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

key64uToKey allows you to convert a base64 url-file safe key string to a
byte string

**key64u** (*required*)- base64 ulr-file safe string

**returns** - byte string

Example
^^^^^^^

.. code:: python

    import pydidery.lib.generating as gen


    key64u = "nxESHveBmK9RsEkgaZi-cNPvW0zO-ujOWEW7oKb7EYI="

    # convert the key
    key = gen.key64uToKey(key64u)

    print(key)

Output
^^^^^^

::

    b'\x9f\x11\x12\x1e\xf7\x81\x98\xafQ\xb0I i\x98\xbep\xd3\xef[L\xce\xfa\xe8\xceXE\xbb\xa0\xa6\xfb\x11\x82'

generating.keyGen(seed=None):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

keyGen generates a url-file safe base64 public private key pair. If a
seed is not provided libnacl's randombytes() function will be used to
generate a seed.

**seed** (*optional*)- The seed value used during key generation.

**returns** - url-file safe base64 verifier/public key, signing/private
key

Example
^^^^^^^

.. code:: python

    import libnacl
    import pydidery.lib.generating as gen


    seed = libnacl.randombytes(libnacl.crypto_sign_SEEDBYTES)

    # generate key pair with custom seed
    vk, sk = gen.keyGen(seed)
    print(vk)
    print(sk)

    # generate key pair with built in seed
    vk, sk = gen.keyGen()
    print(vk)
    print(sk)

Output
^^^^^^

::

    0RvCaAvHInLezCP97jaHoPokAGfP5LTpwAvcR4YqNxQ=
    qNrFUd0pqLbTLIIo_xXpQFuKrqFJe45GO_dMt_OqPITRG8JoC8cict7MI_3uNoeg-iQAZ8_ktOnAC9xHhio3FA==

    0hZpSyBosXHj52TkceVdJoPGmGt26D5ErAEO0I5m-bg=
    qNjuiN_MijfK8eIvJJ4mf7IRMh7noEK92KAUNXzNPPXSFmlLIGixcePnZORx5V0mg8aYa3boPkSsAQ7Qjmb5uA==

generating.signResource(resource, sKey)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

signResource accepts a byte string and an EdDSA (Ed25519) key in the
form of a byte string and returns a base64 url-file safe signature.

**resource** (*required*)- byte string to be signed **sKey**
(*required*)- signing/private key from EdDSA (Ed25519) key

**returns** - url-file safe base64 signature string

Example
^^^^^^^

.. code:: python

    import pydidery.lib.generating as gen

    # generate key pair with custom seed
    vk, sk = gen.keyGen()
    resource = b'{"data":"Test!"}'

    signature = gen.signResource(resource, sk)

    print(signature)

Output
^^^^^^

::

    D4Z8_zeX42n0H_MQQyZWyQ3gW5me1iL4dZetRvo-0_f3tINIcKWrmrtjTFykWhNhHk36Ur2KlVmkdGRgtp8vDQ==

generating.historyGen(seed=None):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

historyGen generates a new key history dictionary and returns the
history along with all generated keys. If a seed is not provided
libnacl's randombytes() function will be used to generate a seed.

**seed** (*optional*)- The seed value used during key generation.

**returns** - - a history dictionary with an "id", "signer" and
"signers" field - url-file safe base64 verifier/public key string -
url-file safe base64 signing/private key - url-file safe base64
pre-rotated verifier/public key - url-file safe base64 pre-rotated
signing/private key

Example
^^^^^^^

.. code:: python

    import libnacl
    import pydidery.lib.generating as gen

    seed = libnacl.randombytes(libnacl.crypto_sign_SEEDBYTES)

    # generate key pair with custom seed
    history, vk, sk, pvk, psk = gen.historyGen(seed)
    print("History: {}".format(history))
    print("public/verification key: \n{}".format(vk))
    print("private/signing key: \n{}".format(sk))
    print("pre-rotated public/verification key: \n{}".format(pvk))
    print("pre-rotated private/signing key: \n{}".format(psk))

    # generate key pair with built in seed
    history, vk, sk, pvk, psk = gen.historyGen()
    print("History: \n{}".format(history))
    print("public/verification key: \n{}".format(vk))
    print("private/signing key: \n{}".format(sk))
    print("pre-rotated public/verification key: \n{}".format(pvk))
    print("pre-rotated private/signing key: \n{}".format(psk))

Output
^^^^^^

::

    History: {
        'id': 'did:dad:i2ZGgZbsjw0SsZPJLis5sBjBl_FBO9cAk7tOdcCtMt0=', 
        'signer': 0, 
        'signers': [
            'i2ZGgZbsjw0SsZPJLis5sBjBl_FBO9cAk7tOdcCtMt0=', 
            'i2ZGgZbsjw0SsZPJLis5sBjBl_FBO9cAk7tOdcCtMt0='
        ]
    }

    public/verification key: 
    i2ZGgZbsjw0SsZPJLis5sBjBl_FBO9cAk7tOdcCtMt0=

    private/signing key: 
    SiMxYSaGTF2XHx648dqNAIfSOoRfQd-3SbE0sT7WE72LZkaBluyPDRKxk8kuKzmwGMGX8UE71wCTu051wK0y3Q==

    pre-rotated public/verification key: 
    i2ZGgZbsjw0SsZPJLis5sBjBl_FBO9cAk7tOdcCtMt0=

    pre-rotated private/signing key: 
    SiMxYSaGTF2XHx648dqNAIfSOoRfQd-3SbE0sT7WE72LZkaBluyPDRKxk8kuKzmwGMGX8UE71wCTu051wK0y3Q==



    History: {
        'id': 'did:dad:ognfYHtL5HLAQUox5jODI2L5R8O3coGsN3ZKEfrKRqc=', 
        'signer': 0, 
        'signers': [
            'ognfYHtL5HLAQUox5jODI2L5R8O3coGsN3ZKEfrKRqc=', 
            'FuacQCdWImyzZwcMkIxKjoH1Kp_4SY6KsGWhc83fGrc='
        ]
    }

    public/verification key: 
    ognfYHtL5HLAQUox5jODI2L5R8O3coGsN3ZKEfrKRqc=

    private/signing key: 
    0rmt38sxKXWwwMfhGzGmt5tCNcLOsW4_kYu5zULbGVeiCd9ge0vkcsBBSjHmM4MjYvlHw7dygaw3dkoR-spGpw==

    pre-rotated public/verification key: 
    FuacQCdWImyzZwcMkIxKjoH1Kp_4SY6KsGWhc83fGrc=

    pre-rotated private/signing key: 
    t9CMQT-u3VhAj7R-GuZ_UaScc_RGE7E-YgJxfIhMLAoW5pxAJ1YibLNnBwyQjEqOgfUqn_hJjoqwZaFzzd8atw==
