from ioflo.aid import getConsole
from ioflo.aid import odict
from ioflo.base import doify


console = getConsole()


@doify('UploadData', ioinits=odict(test=""))
def uploadData(self):
    console.terse("UPLOAD!")


@doify('Rotation', ioinits=odict(test=""))
def rotation(self):
    pass


@doify('Retrieval', ioinits=odict(test=""))
def retrieval(self):
    pass
