# Didery.py
Didery.py is a python library and command line wrapper for communicating with didery servers.  It handles broadcasting data and polling data from remote didery servers and verifying consensus on the returned data.

## Getting Started
You will need python 3.6 and libsodium installed to run didery.py. You can find python 3.6 [here](https://www.python.org/downloads/)  and libsodium [here](https://download.libsodium.org/doc/installation/).  It is recommended that you also setup a python virtual environment as shown [here](http://cewing.github.io/training.python_web/html/presentations/venv_intro.html).

## Installation
To install didery.py start your virtual environment and run the command below:
```
$ pip install -e didery.py/
```

## Usage
To see the command line options use the command below:
```
$ didery.py --help
```

```
Usage: didery.py [OPTIONS] CONFIG

Options:
  --upload [otp|history]         Choose the type of upload 'otp' or 'history'.
  --rotate                       Send rotation event to didery servers.
  --retrieve [otp|history]       Retrieve 'otp' or 'history' data.
  -d, --data PATH                Specify path to data file.
  -c, --consensus INTEGER RANGE  Threshold(%) at which consensus is reached.
  -v                             Verbosity of console output. There are 5
                                 verbosity levels from '' to '-vvvv.'
  --help                         Show this message and exit.
```

### Config File
The CLI requires a path to a config file with the data shown below.  Because of the sensitive nature of the data signing keys should not be stored in this file and will be deleted upon exit of didery.py.  **DO NOT** enter a signing key **UNLESS** it is required for the current task.
```json
{
	"servers": [],
	"did":"",
	"current_sk":"",   //optional for data retrieval
	"rotation_sk":"",  //optional for inception event
	"consensus": 50    //optional for non retrieval requests
}
``` 
**"servers"** [list] _required_
 - A list of server address strings.  This must be supplied so the library knows what servers to broadcast and poll from.
 
**"did"** [string] _required_
- [Decentralized Identifier](https://w3c-ccg.github.io/did-spec/).  This is needed to locate or store a resource.

**"current_sk"** [string]
- The current signing key.  Should only be supplied when uploading data like an otp blob, rotation history, or rotation event.

**"rotation_sk"** [string]
- The pre rotated signing key.  This should only be supplied if you are starting a rotation event.

**"consensus"** [int]
- The percent at which consensus is reached.  Value should be between 0 and 100.  You can also use the command line option -c, --consensus instead of this field.  Didery.py will default to the cli value when given both options.

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
