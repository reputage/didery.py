import pytest

from diderypy.lib import didering


def testDidGenWithNone():
    vk = None

    assert didering.didGen(vk) is None


def testDidGen():
    vk = b'\xfdv\xae\xeb\xe7\x08Q\xaf\xedY\xcf\x8b"\xfc\xa6\xeb\x1c@\x89}\xdb\xed\x16\xa5\xb6\x88\x18\xc8\x1a%O\x83'

    did = didering.didGen(vk)

    assert did == "did:dad:_Xau6-cIUa_tWc-LIvym6xxAiX3b7RaltogYyBolT4M="


def testDidGenWithMethod():
    vk = b'\xfdv\xae\xeb\xe7\x08Q\xaf\xedY\xcf\x8b"\xfc\xa6\xeb\x1c@\x89}\xdb\xed\x16\xa5\xb6\x88\x18\xc8\x1a%O\x83'
    method = "dad"
    did = didering.didGen(vk, method)

    assert did == "did:dad:_Xau6-cIUa_tWc-LIvym6xxAiX3b7RaltogYyBolT4M="

    method = "igo"
    did = didering.didGen(vk, method)

    assert did == "did:igo:_Xau6-cIUa_tWc-LIvym6xxAiX3b7RaltogYyBolT4M="


def testDidGen64WithNone():
    vk = None

    assert didering.didGen64(vk) is None


def testDidGen64():
    vk = "nxESHveBmK9RsEkgaZi-cNPvW0zO-ujOWEW7oKb7EYI="

    did = didering.didGen64(vk)

    assert did == "did:dad:nxESHveBmK9RsEkgaZi-cNPvW0zO-ujOWEW7oKb7EYI="


def testDidGen64WithMethod():
    vk = "nxESHveBmK9RsEkgaZi-cNPvW0zO-ujOWEW7oKb7EYI="
    method = "dad"
    did = didering.didGen64(vk, method)

    assert did == "did:dad:nxESHveBmK9RsEkgaZi-cNPvW0zO-ujOWEW7oKb7EYI="

    method = "igo"
    did = didering.didGen64(vk, method)

    assert did == "did:igo:nxESHveBmK9RsEkgaZi-cNPvW0zO-ujOWEW7oKb7EYI="


def testExtractDidParts():
    did1 = "did:dad:nxESHveBmK9RsEkgaZi-cNPvW0zO-ujOWEW7oKb7EYI="
    did2 = "did:igo:nxESHveBmK9RsEkgaZi-cNPvW0zO-ujOWEW7oKb7EYI="

    prefix, method, verkey = didering.extractDidParts(did1)

    assert prefix == "did"
    assert method == "dad"
    assert verkey == "nxESHveBmK9RsEkgaZi-cNPvW0zO-ujOWEW7oKb7EYI="

    prefix, method, verkey = didering.extractDidParts(did2)

    assert prefix == "did"
    assert method == "igo"
    assert verkey == "nxESHveBmK9RsEkgaZi-cNPvW0zO-ujOWEW7oKb7EYI="


def testExtractDidPartsWithError():
    # missing prefix
    did = "dad:nxESHveBmK9RsEkgaZi-cNPvW0zO-ujOWEW7oKb7EYI="
    with pytest.raises(ValueError) as ex:
        didering.extractDidParts(did)

    # missing method
    did = "did:nxESHveBmK9RsEkgaZi-cNPvW0zO-ujOWEW7oKb7EYI="
    with pytest.raises(ValueError) as ex:
        didering.extractDidParts(did)

    # missing verification key
    did = "did:dad"
    with pytest.raises(ValueError) as ex:
        didering.extractDidParts(did)

    # blank method
    did = "did::nxESHveBmK9RsEkgaZi-cNPvW0zO-ujOWEW7oKb7EYI="
    with pytest.raises(ValueError) as ex:
        didering.extractDidParts(did)


def testValidateDid():
    did = "did:dad:nxESHveBmK9RsEkgaZi-cNPvW0zO-ujOWEW7oKb7EYI="

    rdid, key = didering.validateDid(did)

    assert rdid == did
    assert key == "nxESHveBmK9RsEkgaZi-cNPvW0zO-ujOWEW7oKb7EYI="


def testValidateDidWithMethod():
    did = "did:igo:nxESHveBmK9RsEkgaZi-cNPvW0zO-ujOWEW7oKb7EYI="

    rdid, key = didering.validateDid(did, "igo")

    assert rdid == did
    assert key == "nxESHveBmK9RsEkgaZi-cNPvW0zO-ujOWEW7oKb7EYI="


def testValidateDidWithErrors():
    # missing prefix
    did = "dad:nxESHveBmK9RsEkgaZi-cNPvW0zO-ujOWEW7oKb7EYI="
    with pytest.raises(ValueError) as ex:
        didering.validateDid(did)

    # missing method
    did = "did:nxESHveBmK9RsEkgaZi-cNPvW0zO-ujOWEW7oKb7EYI="
    with pytest.raises(ValueError) as ex:
        didering.validateDid(did)

    # missing verification key
    did = "did:dad"
    with pytest.raises(ValueError) as ex:
        didering.validateDid(did)

    # blank method
    did = "did::nxESHveBmK9RsEkgaZi-cNPvW0zO-ujOWEW7oKb7EYI="
    with pytest.raises(ValueError) as ex:
        didering.validateDid(did)

    # invalid prefix
    did = "dad:dad:nxESHveBmK9RsEkgaZi-cNPvW0zO-ujOWEW7oKb7EYI="
    with pytest.raises(ValueError) as ex:
        didering.validateDid(did)

    # wrong method
    did = "dad:igo:nxESHveBmK9RsEkgaZi-cNPvW0zO-ujOWEW7oKb7EYI="
    with pytest.raises(ValueError) as ex:
        didering.validateDid(did, "dad")
