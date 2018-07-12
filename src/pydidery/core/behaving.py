from ioflo.aid import getConsole
from ioflo.aid import odict
from ioflo.base import doify


from ..lib import historying as hist
from ..lib import otping as otp


def outputResult(result, console, verbosity):
    successful = 0
    console.concise("Result: \n")
    for url, data in result.items():
        if verbosity == console.Wordage.profuse:
            console.profuse("{}:\t{}\n".format(url, data))
        if verbosity == console.Wordage.concise:
            console.concise("{}:\tHTTP_{}\n".format(url, data[1]))
        if 300 > data[1] >= 200:
            successful += 1

    console.terse("\n{}/{} requests succeeded.\n".format(successful, len(result)))


@doify('Incept', ioinits=odict(
    servers="",
    data="",
    sk="",
    test="",
    complete=odict(value=False),
    verbosity="",
    start=""
))
def incept(self):
    if not self.start.value:
        self.complete.value = True
        return

    console = getConsole("didery.py", verbosity=self.verbosity.value)

    console.terse("\n")
    console.concise("Servers:\n{}\n\n".format(self.servers.value))
    console.profuse("Data:\n{}\n\n".format(self.data.value))

    result = hist.postHistory(self.data.value, self.sk.value, self.servers.value)

    outputResult(result, console, self.verbosity.value)

    self.complete.value = True


@doify('Upload', ioinits=odict(
    servers="",
    data="",
    sk="",
    test="",
    complete=odict(value=False),
    verbosity="",
    start=""
))
def upload(self):
    if not self.start.value:
        self.complete.value = True
        return

    console = getConsole("didery.py", verbosity=self.verbosity.value)

    console.terse("\n")
    console.concise("Servers:\n{}\n\n".format(self.servers.value))
    console.profuse("Data:\n{}\n\n".format(self.data.value))

    result = otp.postOtpBlob(self.data.value, self.sk.value, self.servers.value)

    outputResult(result, console, self.verbosity.value)

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
    if not self.start.value:
        self.complete.value = True
        return

    console = getConsole("didery.py", verbosity=self.verbosity.value)

    console.terse("\n")
    console.concise("Servers:\n{}\n\n".format(self.servers.value))
    console.profuse("Data:\n{}\n\n".format(self.data.value))

    result = hist.putHistory(self.did.value, self.data.value, self.sk.value, self.psk.value, self.servers.value)

    outputResult(result, console, self.verbosity.value)

    self.complete.value = True


@doify('Update', ioinits=odict(
    servers="",
    data="",
    did="",
    sk="",
    test="",
    complete=odict(value=False),
    verbosity="",
    start=""
))
def update(self):
    if not self.start.value:
        self.complete.value = True
        return

    console = getConsole("didery.py", verbosity=self.verbosity.value)

    console.terse("\n")
    console.concise("Servers:\n{}\n\n".format(self.servers.value))
    console.profuse("Data:\n{}\n\n".format(self.data.value))

    print(self.data.value)

    result = otp.putOtpBlob(self.did.value, self.data.value, self.sk.value, self.servers.value)

    outputResult(result, console, self.verbosity.value)

    self.complete.value = True


@doify('Retrieval', ioinits=odict(
    servers="",
    did="",
    test="",
    complete=odict(value=False),
    verbosity="",
    start=""
))
def retrieval(self):
    if not self.start.value:
        self.complete.value = True
        return

    console = getConsole("didery.py", verbosity=self.verbosity.value)

    console.terse("\n")
    console.concise("Servers: {}\n".format(self.servers.value))
    console.profuse("DID: {}\n".format(self.did.value))

    result = hist.getDidHistory(self.did.value, self.servers.value)

    if result:
        console.terse("Result: \nData:\t{}\nSignatures:\t{}\n".format(result["history"], result["signatures"]))
    else:
        console.terse("Consensus Failed.\n")

    self.complete.value = True


@doify('Download', ioinits=odict(
    servers="",
    did="",
    test="",
    complete=odict(value=False),
    verbosity="",
    start=""
))
def download(self):
    if not self.start.value:
        self.complete.value = True
        return

    console = getConsole("didery.py", verbosity=self.verbosity.value)

    console.terse("\n")
    console.concise("Servers: {}\n".format(self.servers.value))
    console.profuse("DID: {}\n".format(self.did.value))

    result = otp.getOtpBlob(self.did.value, self.servers.value)

    if result:
        console.terse("Result: \nData:\t{}\nSignatures:\t{}\n".format(result["otp_data"], result["signature"]))
    else:
        console.terse("Consensus Failed.\n")

    self.complete.value = True
