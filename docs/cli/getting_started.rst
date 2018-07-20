Getting Started
===============

You will need python 3.6 and libsodium installed to run didery.py. You
can find python 3.6 `here <https://www.python.org/downloads/>`__ and
libsodium `here <https://download.libsodium.org/doc/installation/>`__.
It is recommended that you also setup a python virtual environment as
shown
`here <http://cewing.github.io/training.python_web/html/presentations/venv_intro.html>`__.

Installation
------------

To install didery.py start your virtual environment and run the command
below:

::

    $ pip install -e didery.py/

Usage
-----

To see the command line options use the command below:

::

    $ didery --help

::

    Usage: didery [OPTIONS] CONFIG

    Options:
      --incept    Send a key rotation history inception event.
      --upload    Upload a new otp encrypted private key.
      --rotate    Rotate public/private key pairs.
      --update    Update otp encrypted private key.
      --retrieve  Retrieve key rotation history.
      --download  Download otp encrypted private key.
      -v          Verbosity of console output. There are 5 verbosity levels from
                  '' to '-vvvv.'
      --help      Show this message and exit.

Config File
~~~~~~~~~~~

The CLI requires a path to a json formatted config file with a list of
didery endpoints as shown below.

.. code:: json

    {
        "servers": ["http://localhost:8080", "http://localhost:8000"]
    }

**"servers"** [list] *required* - A list of server address strings. This
must be supplied so the library knows what servers to broadcast and poll
from. To determine if there is a consensus on polling a 2/3 of the
servers must return matching responses.

Data File
~~~~~~~~~

For certain commands it is necessary to supply a data file. The file
should be json formatted and will contain either the rotation history or
the `one time pad <https://en.wikipedia.org/wiki/One-time_pad>`__\ (otp)
encrypted blob. The data file is required for the following options:

--upload

--rotate

The file should follow the format below for history data:

.. code:: json

    {
        "history": {
            "id": "did:dad:Qt27fThWoNZsa88VrTkep6H-4HA8tr54sHON1vWl6FE=",
            "signer": 0,
            "signers": 
            [
                "Qt27fThWoNZsa88VrTkep6H-4HA8tr54sHON1vWl6FE=",
                "Xq5YqaL6L48pf0fu7IUhL0JRaU2_RxFP0AL43wYn148="
            ]
        }
    }

**"id"** [string] *required* - Decentralized identifier
`(DID) <https://w3c-ccg.github.io/did-spec/>`__.

**"signer"** [integer] *required* - 0 based index into signers field.
Rotation events signer field will always be 1 or greater.

**"signers"** [list] *required* - List of all public keys. Must contain
at least two keys for --upload and 3 or more for --rotation.

The file should follow the format below for
`otp <https://en.wikipedia.org/wiki/One-time_pad>`__ data:

.. code:: json

    {
        "otp": {
            "blob": "AeYbsHot0pmdWAcgTo5sD8iAuSQAfnH5U6wiIGpVNJQQoYKBYrPPxAoIc1i5SHCIDS8KFFgf8i0tDq8XGizaCgo9yjuKHHNJZFi0QD9K6Vpt6fP0XgXlj8z_4D-7s3CcYmuoWAh6NVtYaf_GWw_2sCrHBAA2mAEsml3thLmu50Dw",
            "id": "did:dad:Qt27fThWoNZsa88VrTkep6H-4HA8tr54sHON1vWl6FE="
        }
    }

| **"id"** [string] *required*
| - Decentralized identifier
  `(DID) <https://w3c-ccg.github.io/did-spec/>`__.

| **"blob"** [string] *required*
| - `otp <https://en.wikipedia.org/wiki/One-time_pad>`__ encrypted
  private keys.
