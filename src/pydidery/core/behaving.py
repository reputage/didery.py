from ioflo.aid import getConsole
from ioflo.aid import odict
from ioflo.base import doify


from ..lib import historying as hist
from ..lib import otping as otp


@doify('Upload', ioinits=odict(
    servers="",
    data="",
    sk="",
    type="",
    test="",
    complete=odict(value=False),
    verbosity="",
    start=""
))
def upload(self):
    verbosity = self.verbosity.value if self.start.value else 0

    console = getConsole("didery.py", verbosity=verbosity)

    console.terse("\n")
    console.concise("Servers:\n{}\n\n".format(self.servers.value))
    console.profuse("Data:\n{}\n\n".format(self.data.value))
    result = {}

    if self.type.value == "history":
        result = hist.postHistory(self.data.value, self.sk.value, self.servers.value)
    elif self.type.value == "otp":
        result = otp.postOtpBlob(self.data.value, self.sk.value, self.servers.value)

    successful = 0
    console.concise("Result: \n")
    for url, data in result.items():
        if self.verbosity.value == console.Wordage.profuse:
            console.profuse("{}:\t{}\n".format(url, data))
        if self.verbosity.value == console.Wordage.concise:
            console.concise("{}:\tHTTP_{}\n".format(url, data[1]))
        if 300 > data[1] >= 200:
            successful += 1

    console.terse("\n{}/{} requests succeeded.\n".format(successful, len(result)))

    self.complete.value = True


@doify('Rotation', ioinits=odict(
    servers="",
    data="",
    did="",
    sk="",
    psk="",
    test="",
    complete=odict(value=False),
    verbosity="",
    start=""
))
def rotation(self):
    verbosity = self.verbosity.value if self.start.value else 0

    console = getConsole("didery.py", verbosity=verbosity)

    console.terse("\n")
    console.concise("Servers:\n{}\n\n".format(self.servers.value))
    console.profuse("Data:\n{}\n\n".format(self.data.value))

    if self.servers.value is not None:
        result = hist.putHistory(self.did.value, self.data.value, self.sk.value, self.psk.value, self.servers.value)
    else:
        result = {}

    successful = 0
    console.concise("Result: \n")
    for url, data in result.items():
        if self.verbosity.value == console.Wordage.profuse:
            console.profuse("{}:\t{}\n".format(url, data))
        if self.verbosity.value == console.Wordage.concise:
            console.concise("{}:\tHTTP_{}\n".format(url, data[1]))
        if 300 > data[1] >= 200:
            successful += 1

    console.terse("\n{}/{} requests succeeded.\n".format(successful, len(result)))

    self.complete.value = True


@doify('Retrieval', ioinits=odict(
    servers="",
    did="",
    type="",
    test="",
    complete=odict(value=False),
    verbosity="",
    start=""
))
def retrieval(self):
    verbosity = self.verbosity.value if self.start.value else 0

    console = getConsole("didery.py", verbosity=verbosity)

    console.terse("\n")
    console.concise("Servers: {}\n".format(self.servers.value))
    console.profuse("DID: {}\n".format(self.did.value))
    result = {}

    if self.type.value == "history":
        result = hist.getDidHistory(self.did.value, self.servers.value)
    elif self.type.value == "otp_data":
        result = otp.getOtpBlob(self.did.value, self.servers.value)

    if result:
        if self.type.value == "history":
            console.terse("Result: \nData:\t{}\nSignatures:\t{}\n".format(result["history"], result["signatures"]))
        elif self.type.value == "otp_data":
            console.terse("Result: \nData:\t{}\nSignatures:\t{}\n".format(result["otp_data"], result["signature"]))
    else:
        console.terse("Consensus Failed.\n")

    self.complete.value = True
