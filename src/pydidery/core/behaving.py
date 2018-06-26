from ioflo.aid import getConsole
from ioflo.aid import odict
from ioflo.base import doify


from ..lib import historying as hist


console = getConsole()


@doify('Upload', ioinits=odict(
    servers="",
    data="",
    did="",
    sk="",
    type="",
    test=""
))
def upload(self):
    console.terse("\n")
    console.terse("Servers: {}\n".format(self.servers.value))
    console.terse("Data: {}\n".format(self.data.value))
    console.terse("\n")

    if self.type.value == "history":
        result = hist.postHistory(self.data.value, self.sk.value, self.servers.value[0])
    else:
        # TODO build post otp blob request
        result = ""

    console.terse("Result: {}\n\n".format(result))


@doify('Rotation', ioinits=odict(
    servers="",
    data="",
    did="",
    sk="",
    psk="",
    test=""
))
def rotation(self):
    console.terse("\n")
    console.terse("Servers: {}\n".format(self.servers.value))
    console.terse("Data: {}\n".format(self.data.value))
    console.terse("\n")

    if self.servers.value is not None:
        result = hist.putHistory(self.did.value, self.data.value, self.sk.value, self.psk.value, self.servers.value[0])
    else:
        result = ""

    console.terse("Result: {}\n\n".format(result))


@doify('Retrieval', ioinits=odict(
    servers="",
    did="",
    type="",
    test=""
))
def retrieval(self):
    console.terse("\n")
    console.terse("Servers: {}\n".format(self.servers.value))
    console.terse("DID: {}\n".format(self.did.value))
    console.terse("\n")

    if self.type.value == "history":
        result = hist.getDidHistory(self.did.value, self.servers.value[0])
    else:
        # TODO build get otp blob request
        result = ""

    console.terse("Result: {}\n\n".format(result))
