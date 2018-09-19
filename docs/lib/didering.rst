didering.py
===========

This module provides various
`DID <https://w3c-ccg.github.io/did-spec/>`__ generation and
manipulation functions for use with the didery server.

didering.didGen(vk, [method])
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

didGen accepts an EdDSA (Ed25519) key in the form of a byte string and
returns a DID.

| **vk** (*required*)- 32 byte verifier/public key from EdDSA (Ed25519)
  key
| **method** (*optional*) - `W3C did
  method <https://w3c-ccg.github.io/did-spec/#specific-did-method-schemes>`__
  string. Defaults to "dad".

**returns** - `W3C DID <https://w3c-ccg.github.io/did-spec/>`__ string

Example
^^^^^^^

.. code:: python

    import diderypy.lib.didering as did


    vk = b'\xfdv\xae\xeb\xe7\x08Q\xaf\xedY\xcf\x8b"\xfc\xa6\xeb\x1c@\x89}\xdb\xed\x16\xa5\xb6\x88\x18\xc8\x1a%O\x83'

    # use the default method
    did1 = did.didGen(vk)

    # or you can specify a method like igo
    did2 = did.didGen(vk, "igo")

    print(did1)
    print(did2)

Output
^^^^^^

::

    did:dad:_Xau6-cIUa_tWc-LIvym6xxAiX3b7RaltogYyBolT4M=
    did:igo:_Xau6-cIUa_tWc-LIvym6xxAiX3b7RaltogYyBolT4M=

didering.didGen64(vk64u, [method]):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

didGen accepts a url-file safe base64 key in the form of a string and
returns a DID.

| **vk64u** (*required*)- base64 url-file safe verifier/public key from
  EdDSA (Ed25519) key
| **method** (*optional*) - `W3C did
  method <https://w3c-ccg.github.io/did-spec/#specific-did-method-schemes>`__
  string. Defaults to "dad"

**returns** - `W3C DID <https://w3c-ccg.github.io/did-spec/>`__ string

Example
^^^^^^^

.. code:: python

    import diderypy.lib.didering as did


    vk = "nxESHveBmK9RsEkgaZi-cNPvW0zO-ujOWEW7oKb7EYI="

    # use the default method
    did1 = did.didGen64(vk)

    # or you can specify a method like igo
    did2 = did.didGen64(vk, "igo")

    print(did1)
    print(did2)

Output
^^^^^^

::

    did:dad:nxESHveBmK9RsEkgaZi-cNPvW0zO-ujOWEW7oKb7EYI=
    did:igo:nxESHveBmK9RsEkgaZi-cNPvW0zO-ujOWEW7oKb7EYI=

didering.extractDidParts(did):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

extractDidParts parses and returns a tuple containing the prefix method
and key string contained in the supplied `W3C
DID <https://w3c-ccg.github.io/did-spec/>`__ string. If the supplied
string does not fit the pattern pre:method:keystr a ValueError is
raised.

**did** (*required*)- `W3C DID <https://w3c-ccg.github.io/did-spec/>`__
string

**returns** - (pre, method, key string) a tuple containing the did
parts.

Example
^^^^^^^

.. code:: python

    import diderypy.lib.didering as did


    did1 = "did:dad:nxESHveBmK9RsEkgaZi-cNPvW0zO-ujOWEW7oKb7EYI="
    did2 = "did:igo:nxESHveBmK9RsEkgaZi-cNPvW0zO-ujOWEW7oKb7EYI="


    result1 = did.extractDidParts(did1)
    result2 = did.extractDidParts(did2)

    print(result1)
    print(result2)

Output
^^^^^^

::

    ('did', 'dad', 'nxESHveBmK9RsEkgaZi-cNPvW0zO-ujOWEW7oKb7EYI=')
    ('did', 'igo', 'nxESHveBmK9RsEkgaZi-cNPvW0zO-ujOWEW7oKb7EYI=')

didering.validateDid(did, [method]):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

validateDid accepts a `W3C DID <https://w3c-ccg.github.io/did-spec/>`__
string and an optional method argument. It returns the DID as well as
the public/verifier key contained in the did. If the DID is invalid a
ValueError is raised.

| **did** (*required*)- `W3C
  DID <https://w3c-ccg.github.io/did-spec/>`__ string
| **method** (*optional*) - `W3C did
  method <https://w3c-ccg.github.io/did-spec/#specific-did-method-schemes>`__
  string. Defaults to "dad"

**returns** - Tuple with `W3C
DID <https://w3c-ccg.github.io/did-spec/>`__ string, and the did's
verifier/public key

Example
^^^^^^^

.. code:: python

    import diderypy.lib.didering as did


    did1 = "did:dad:nxESHveBmK9RsEkgaZi-cNPvW0zO-ujOWEW7oKb7EYI="
    did2 = "did:igo:nxESHveBmK9RsEkgaZi-cNPvW0zO-ujOWEW7oKb7EYI="

    # use the default method
    result1 = did.validateDid(did1)

    # or you can specify a method like igo
    result2 = did.validateDid(did2, "igo")

    print(result1)
    print(result2)

Output
^^^^^^

::

    ('did:dad:nxESHveBmK9RsEkgaZi-cNPvW0zO-ujOWEW7oKb7EYI=', 'nxESHveBmK9RsEkgaZi-cNPvW0zO-ujOWEW7oKb7EYI=')
    ('did:igo:nxESHveBmK9RsEkgaZi-cNPvW0zO-ujOWEW7oKb7EYI=', 'nxESHveBmK9RsEkgaZi-cNPvW0zO-ujOWEW7oKb7EYI=')
