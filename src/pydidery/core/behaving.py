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

    result = hist.putHistory(self.data.value, self.sk.value, self.psk.value, self.servers.value)

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

    result = otp.putOtpBlob(self.data.value, self.sk.value, self.servers.value)

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

    data, results = hist.getHistory(self.did.value, self.servers.value)

    if data:
        console.terse("Result: \nData:\t{}\nSignatures:\t{}\n".format(data["history"], data["signatures"]))
        for url, result in results.items():
            console.verbose("{}:\t{}\n".format(url, result))
    else:
        console.terse("Consensus Failed.\n")
        for url, result in results.items():
            console.concise("{}:\t{}\n".format(url, result))

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

    data, results = otp.getOtpBlob(self.did.value, self.servers.value)

    if data:
        console.terse("Result: \nData:\t{}\nSignatures:\t{}\n".format(data["otp_data"], data["signatures"]))
        for url, result in results.items():
            console.verbose("{}:\t{}\n".format(url, result))
    else:
        console.terse("Consensus Failed.\n")
        for url, result in results.items():
            console.concise("{}:\t{}\n".format(url, result))

    self.complete.value = True


@doify('Delete', ioinits=odict(
    servers="",
    did="",
    sk="",
    test="",
    complete=odict(value=False),
    verbosity="",
    start=""
))
def delete(self):
    if not self.start.value:
        self.complete.value = True
        return

    console = getConsole("didery.py", verbosity=self.verbosity.value)

    console.terse("\n")
    console.concise("Servers: {}\n".format(self.servers.value))
    console.profuse("DID: {}\n".format(self.did.value))

    result = hist.deleteHistory(self.did.value, self.sk.value, self.servers.value)

    outputResult(result, console, self.verbosity.value)

    self.complete.value = True


@doify('Remove', ioinits=odict(
    servers="",
    did="",
    sk="",
    test="",
    complete=odict(value=False),
    verbosity="",
    start=""
))
def remove(self):
    if not self.start.value:
        self.complete.value = True
        return

    console = getConsole("didery.py", verbosity=self.verbosity.value)

    console.terse("\n")
    console.concise("Servers: {}\n".format(self.servers.value))
    console.profuse("DID: {}\n".format(self.did.value))

    result = otp.removeOtpBlob(self.did.value, self.sk.value, self.servers.value)

    outputResult(result, console, self.verbosity.value)

    self.complete.value = True
