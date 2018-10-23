try:
    import simplejson as json
except ImportError:
    import json

from urllib.parse import urlparse
from ioflo.aid import getConsole
from ioflo.aid import odict
from ioflo.base import doify


from ..lib import historying as hist
from ..lib import otping as otp
from ..lib import history_eventing as event


def outputSetupInfo(console, servers, data=None, did=None):
    console.terse("\n")
    console.concise("Servers:\n{}\n\n".format(json.dumps(servers, indent=4)))

    if data:
        console.profuse("Data:\n{}\n\n".format(data))

    if did:
        console.profuse("Retrieving DID:\t\t{}\n\n".format(did))


def outputPushedResult(result, console, verbosity):
    successful = 0
    profuse = ""
    concise = ""

    for url, data in result.items():
        parsed_url = urlparse(url)
        f_url = "{}://{}:".format(parsed_url.scheme, parsed_url.netloc).ljust(34)
        if verbosity == console.Wordage.profuse:
            if data.status < 400 and data.status != 0:
                profuse += "{} status: {}\t{}\n".format(f_url, repr(data.status).ljust(9), data.response)
            else:
                if data.status == 0:
                    profuse += "{} status: Timed Out\n".format(f_url)
                else:
                    profuse += "{} status: {}\n".format(f_url, repr(data.status).ljust(9))

        if verbosity == console.Wordage.concise:
            if data.status == 0:
                concise += "{} status: Timed Out\n".format(f_url)
            else:
                concise += "{} status: HTTP_{}\n".format(f_url, repr(data.status).ljust(2))

        if 300 > data.status >= 200:
            successful += 1

    console.terse("\n{}/{} requests succeeded.\n\n".format(successful, len(result)))
    console.concise(concise)
    console.profuse(profuse)


def outputPulledResult(data, results, console):
    if data:
        formatted_data = json.dumps(data, indent=4)

        console.terse("Data:\t{}\n".format(formatted_data))

        for url, result in results.items():
            console.verbose("{}\n".format(result))
    else:
        console.terse("Consensus Failed.\n\n")

        for url, result in results.items():
            console.concise("{}\n".format(result))


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

    outputSetupInfo(console, self.servers.value, data=self.data.value)

    result = hist.postHistory(self.data.value, self.sk.value, self.servers.value)

    outputPushedResult(result, console, self.verbosity.value)

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

    outputSetupInfo(console, self.servers.value, data=self.data.value)

    result = otp.postOtpBlob(self.data.value, self.sk.value, self.servers.value)

    outputPushedResult(result, console, self.verbosity.value)

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

    outputSetupInfo(console, self.servers.value, data=self.data.value)

    result = hist.putHistory(self.data.value, self.sk.value, self.psk.value, self.servers.value)

    outputPushedResult(result, console, self.verbosity.value)

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

    outputSetupInfo(console, self.servers.value, data=self.data.value)

    result = otp.putOtpBlob(self.data.value, self.sk.value, self.servers.value)

    outputPushedResult(result, console, self.verbosity.value)

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

    outputSetupInfo(console, self.servers.value, did=self.did.value)

    data, results = hist.getHistory(self.did.value, self.servers.value)

    outputPulledResult(data, results, console)

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

    outputSetupInfo(console, self.servers.value, did=self.did.value)

    data, results = otp.getOtpBlob(self.did.value, self.servers.value)

    outputPulledResult(data, results, console)

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

    outputSetupInfo(console, self.servers.value, did=self.did.value)

    result = hist.deleteHistory(self.did.value, self.sk.value, self.servers.value)

    outputPushedResult(result, console, self.verbosity.value)

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

    outputSetupInfo(console, self.servers.value, did=self.did.value)

    result = otp.removeOtpBlob(self.did.value, self.sk.value, self.servers.value)

    outputPushedResult(result, console, self.verbosity.value)

    self.complete.value = True


@doify('Events', ioinits=odict(
    servers="",
    did="",
    test="",
    complete=odict(value=False),
    verbosity="",
    start=""
))
def events(self):
    if not self.start.value:
        self.complete.value = True
        return

    console = getConsole("didery.py", verbosity=self.verbosity.value)

    outputSetupInfo(console, self.servers.value, did=self.did.value)

    data, results = event.getHistoryEvents(self.did.value, self.servers.value)

    outputPulledResult(data, results, console)

    self.complete.value = True
