![didery logo](https://github.com/reputage/didery.js/blob/dev/logo/didery.png)

[![Documentation Status](https://readthedocs.org/projects/diderypy/badge/?version=latest)](https://diderypy.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://travis-ci.org/reputage/didery.py.svg?branch=master)](https://travis-ci.org/reputage/didery.py)

# Didery.py
Didery.py is a python library and command line wrapper for communicating with didery servers.  It handles broadcasting data and polling data from remote didery servers and verifying consensus on the returned data.

## Didery.py Python Library
You can find the docs for the library [here](https://diderypy.readthedocs.io/en/latest/) 

## Getting Started With The CLI
You will need python 3.6 and libsodium installed to run didery.py. You can find python 3.6 [here](https://www.python.org/downloads/)  and libsodium [here](https://download.libsodium.org/doc/installation/).  It is recommended that you also setup a python virtual environment as shown [here](http://cewing.github.io/training.python_web/html/presentations/venv_intro.html).

## Installation
To install didery.py start your virtual environment and run the command below:
```
$ pip install -e didery.py/
```

## Usage
To see the command line options use the command below:
```
$ didery --help
```

```
Usage: didery [OPTIONS] CONFIG

Options:
  -i, --incept    Send a key rotation history inception event.
  -u, --upload    Upload a new otp encrypted private key.
  -r, --rotate    Rotate public/private key pairs.
  -U, --update    Update otp encrypted private key.
  -R, --retrieve  Retrieve key rotation history.
  -d, --download  Download otp encrypted private key.
  -D, --delete    Delete rotation history.
  -m, --remove    Remove otp encrypted private key.
  -e, --events    Pull a record of all history rotation events for a specified
                  did.
  -v              Verbosity of console output. There are 5 verbosity levels
                  from '' to '-vvvv.'
  -M, --mute      Mute all console output except prompts.
  --data PATH     Path to the data file.
  --did TEXT      decentralized identifier(did).
  --help          Show this message and exit.
```

### Config File
The CLI requires a path to a json formatted config file with a list of didery endpoints as shown below.
```json
{
	"servers": ["http://localhost:8080", "http://localhost:8000"]
}
``` 
**"servers"** [list] _required_
 - A list of server address strings.  This must be supplied so the library knows what servers to broadcast and poll from. To determine if there is a consensus on polling a 2/3 of the servers must return matching responses.

### Data File
For certain commands it is necessary to supply a data file.  The file should be json formatted and will contain either the rotation history or the [one time pad](https://en.wikipedia.org/wiki/One-time_pad)(otp) encrypted blob. The data file is required for the following options:

--upload

--rotate

The file should follow the format below for history data:
```json
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
```

**"id"** [string] _required_
 - Decentralized identifier [(DID)](https://w3c-ccg.github.io/did-spec/).

**"signer"** [integer] _required_
 - 0 based index into signers field. Rotation events signer field will always be 1 or greater.

**"signers"** [list] _required_
 - List of all public keys. Must contain at least two keys for --upload and 3 or more for --rotation.

The file should follow the format below for [otp](https://en.wikipedia.org/wiki/One-time_pad) data:
```json
{
    "otp": {
        "blob": "AeYbsHot0pmdWAcgTo5sD8iAuSQAfnH5U6wiIGpVNJQQoYKBYrPPxAoIc1i5SHCIDS8KFFgf8i0tDq8XGizaCgo9yjuKHHNJZFi0QD9K6Vpt6fP0XgXlj8z_4D-7s3CcYmuoWAh6NVtYaf_GWw_2sCrHBAA2mAEsml3thLmu50Dw",
        "id": "did:dad:Qt27fThWoNZsa88VrTkep6H-4HA8tr54sHON1vWl6FE="
    }
}
```

**"id"** [string] _required_  
 - Decentralized identifier [(DID)](https://w3c-ccg.github.io/did-spec/).

**"blob"** [string] _required_  
 - [otp](https://en.wikipedia.org/wiki/One-time_pad) encrypted private keys.
