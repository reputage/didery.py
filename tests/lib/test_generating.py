import libnacl
import pytest

from diderypy.lib import generating as gen
from diderypy.lib import didering
from diderypy.help import signing as sign


def testDidGen():
    seed = libnacl.randombytes(libnacl.crypto_sign_SEEDBYTES)
    vk, sk = libnacl.crypto_sign_seed_keypair(seed)

    did = didering.didGen(vk)

    assert did == "did:dad:{}".format(gen.keyToKey64u(vk))


def testDidGen64():
    vk, sk, did = gen.keyGen()

    did = didering.didGen64(vk)

    assert did == "did:dad:{}".format(vk)


def testKeyToKey64u():
    vk = b'\x8d5\xa8\xbc\xbd\x9a\xf5\xbb\xb0\xd0\x88L\xaf\xca\x96\xe6\x03D\x02@N\x8f\xa97S\x9c\xe9;I\xd8\xcaA'
    vk64 = gen.keyToKey64u(vk)

    exp_vk64 = "jTWovL2a9buw0IhMr8qW5gNEAkBOj6k3U5zpO0nYykE="

    assert vk64 == exp_vk64


def testKey64uToKey():
    vk64 = "jTWovL2a9buw0IhMr8qW5gNEAkBOj6k3U5zpO0nYykE="
    vk = gen.key64uToKey(vk64)

    exp_vk = b'\x8d5\xa8\xbc\xbd\x9a\xf5\xbb\xb0\xd0\x88L\xaf\xca\x96\xe6\x03D\x02@N\x8f\xa97S\x9c\xe9;I\xd8\xcaA'

    assert vk == exp_vk


def testKeyGen():
    vk, sk, did = gen.keyGen()

    assert vk
    assert sk


def testKeyGenWithSeed():
    seed = b'\x8dh\xf3\xa0!\xd1\xcd\xc0b\x8c^\x1d\xbcg>\xe1S\x12\xc7\xcb\xbc\x0eTOz@\xdb} \xba\x06\x04'

    vk, sk, did = gen.keyGen(seed)

    exp_vk = "u8TWIE28yAdu-lGrPHH2ZJ73GxoMBZx-D3cf6RMEaTc="
    exp_sk = "jWjzoCHRzcBijF4dvGc-4VMSx8u8DlRPekDbfSC6BgS7xNYgTbzIB276Uas8cfZknvcbGgwFnH4Pdx_pEwRpNw=="

    assert vk == exp_vk
    assert sk == exp_sk


def testSignResource():
    vk = b'\xbb\xc4\xd6 M\xbc\xc8\x07n\xfaQ\xab<q\xf6d\x9e\xf7\x1b\x1a\x0c\x05\x9c~\x0fw\x1f\xe9\x13\x04i7'
    sk = b'\x8dh\xf3\xa0!\xd1\xcd\xc0b\x8c^\x1d\xbcg>\xe1S\x12\xc7\xcb\xbc\x0eTOz@\xdb} \xba\x06\x04\xbb\xc4\xd6 M\xbc\xc8\x07n\xfaQ\xab<q\xf6d\x9e\xf7\x1b\x1a\x0c\x05\x9c~\x0fw\x1f\xe9\x13\x04i7'
    resource = b'{"data":"TEST!"}'

    signature = sign.signResource(resource, sk)

    exp_signature = "dcYLAFhB6A2kU9XwvEcuV0HUDrFVgiraFEtOMsnP8FfOPebFhMbwIClY6PGdKX6CYJvc-9TwCIeca91dcof1Ag=="

    assert signature == exp_signature


def testHistoryGen():
    history = gen.historyGen()

    assert history
    assert len(history) == 5
    assert "id" in history[0]
    assert history[0]["id"] == "did:dad:{}".format(history[1])
    assert "signer" in history[0]
    assert history[0]["signer"] == 0
    assert "signers" in history[0]
    assert history[0]["signers"][0] == history[1]
    assert history[0]["signers"][1] == history[3]


def testHistoryGenWithSeed():
    seed1 = b'\x8dh\xf3\xa0!\xd1\xcd\xc0b\x8c^\x1d\xbcg>\xe1S\x12\xc7\xcb\xbc\x0eTOz@\xdb} \xba\x06\x04'
    seed2 = b'\x8dh\xf3\xa0!\xd1\xcd\xc0b\x8c^\x1d\xbcg>\xe1S\x11\xc7\xcb\xbc\x0eTOz@\xdb} \xba\x06\x04'

    history = gen.historyGen(seed1, seed2)

    exp_history = (
        {
            'id': 'did:dad:u8TWIE28yAdu-lGrPHH2ZJ73GxoMBZx-D3cf6RMEaTc=',
            'signer': 0,
            'signers': [
                'u8TWIE28yAdu-lGrPHH2ZJ73GxoMBZx-D3cf6RMEaTc=',
                'Tni_GX-7IzHAcBwRfN0YBbKQDmpjEjOfB0Pmiki-hCg='
            ]
        },
        'u8TWIE28yAdu-lGrPHH2ZJ73GxoMBZx-D3cf6RMEaTc=',
        'jWjzoCHRzcBijF4dvGc-4VMSx8u8DlRPekDbfSC6BgS7xNYgTbzIB276Uas8cfZknvcbGgwFnH4Pdx_pEwRpNw==',
        'Tni_GX-7IzHAcBwRfN0YBbKQDmpjEjOfB0Pmiki-hCg=',
        'jWjzoCHRzcBijF4dvGc-4VMRx8u8DlRPekDbfSC6BgROeL8Zf7sjMcBwHBF83RgFspAOamMSM58HQ-aKSL6EKA=='
    )

    assert history == exp_history


def testDidBoxInitExceptions():
    permutations = {
        "1": {
            "seed": b'a\x8a\xb3\x89o\xaf\xc50\xf1$\xe2y\xea\xe1<\xd8G{\x9bEE\xbd\xf4\xe7_\xdf\x96\xb3D\x9f\xe0\xb6',
            "vk": b')\xc8\x00i \xa6\x9b\xb3\x80Ci\xd1\x96]\x05N*b\x96zzng\x12\xe4\x0eH\xc9:\n\xd6\xe5',
            "sk": b'a\x8a\xb3\x89o\xaf\xc50\xf1$\xe2y\xea\xe1<\xd8G{\x9bEE\xbd\xf4\xe7_\xdf\x96\xb3D\x9f\xe0\xb6)\xc8\x00i \xa6\x9b\xb3\x80Ci\xd1\x96]\x05N*b\x96zzng\x12\xe4\x0eH\xc9:\n\xd6\xe5',
            "did": 'did:dad: KcgAaSCmm7OAQ2nRll0FTipilnp6bmcS5A5IyToK1uU =',
            "valid": True
        },
        "2": {
            "seed": None,
            "vk": b')\xc8\x00i \xa6\x9b\xb3\x80Ci\xd1\x96]\x05N*b\x96zzng\x12\xe4\x0eH\xc9:\n\xd6\xe5',
            "sk": b'a\x8a\xb3\x89o\xaf\xc50\xf1$\xe2y\xea\xe1<\xd8G{\x9bEE\xbd\xf4\xe7_\xdf\x96\xb3D\x9f\xe0\xb6)\xc8\x00i \xa6\x9b\xb3\x80Ci\xd1\x96]\x05N*b\x96zzng\x12\xe4\x0eH\xc9:\n\xd6\xe5',
            "did": 'did:dad: KcgAaSCmm7OAQ2nRll0FTipilnp6bmcS5A5IyToK1uU =',
            "valid": True
        },
        "3": {
            "seed": None,
            "vk": None,
            "sk": b'a\x8a\xb3\x89o\xaf\xc50\xf1$\xe2y\xea\xe1<\xd8G{\x9bEE\xbd\xf4\xe7_\xdf\x96\xb3D\x9f\xe0\xb6)\xc8\x00i \xa6\x9b\xb3\x80Ci\xd1\x96]\x05N*b\x96zzng\x12\xe4\x0eH\xc9:\n\xd6\xe5',
            "did": 'did:dad: KcgAaSCmm7OAQ2nRll0FTipilnp6bmcS5A5IyToK1uU =',
            "valid": False,
            "error": 'Both private and public keys required'
        },
        "4": {
            "seed": None,
            "vk": None,
            "sk": None,
            "did": 'did:dad: KcgAaSCmm7OAQ2nRll0FTipilnp6bmcS5A5IyToK1uU =',
            "valid": False,
            "error": 'Keys required with did'
        },
        "5": {
            "seed": None,
            "vk": None,
            "sk": None,
            "did": None,
            "valid": True
        },
        "6": {
            "seed": b'a\x8a\xb3\x89o\xaf\xc50\xf1$\xe2y\xea\xe1<\xd8G{\x9bEE\xbd\xf4\xe7_\xdf\x96\xb3D\x9f\xe0\xb6',
            "vk": None,
            "sk": None,
            "did": None,
            "valid": True
        },
        "7": {
            "seed": b'a\x8a\xb3\x89o\xaf\xc50\xf1$\xe2y\xea\xe1<\xd8G{\x9bEE\xbd\xf4\xe7_\xdf\x96\xb3D\x9f\xe0\xb6',
            "vk": b')\xc8\x00i \xa6\x9b\xb3\x80Ci\xd1\x96]\x05N*b\x96zzng\x12\xe4\x0eH\xc9:\n\xd6\xe5',
            "sk": None,
            "did": None,
            "valid": False,
            "error": 'Both private and public keys required'
        },
        "8": {
            "seed": b'a\x8a\xb3\x89o\xaf\xc50\xf1$\xe2y\xea\xe1<\xd8G{\x9bEE\xbd\xf4\xe7_\xdf\x96\xb3D\x9f\xe0\xb6',
            "vk": b')\xc8\x00i \xa6\x9b\xb3\x80Ci\xd1\x96]\x05N*b\x96zzng\x12\xe4\x0eH\xc9:\n\xd6\xe5',
            "sk": b'a\x8a\xb3\x89o\xaf\xc50\xf1$\xe2y\xea\xe1<\xd8G{\x9bEE\xbd\xf4\xe7_\xdf\x96\xb3D\x9f\xe0\xb6)\xc8\x00i \xa6\x9b\xb3\x80Ci\xd1\x96]\x05N*b\x96zzng\x12\xe4\x0eH\xc9:\n\xd6\xe5',
            "did": None,
            "valid": True
        },
        "9": {
            "seed": b'a\x8a\xb3\x89o\xaf\xc50\xf1$\xe2y\xea\xe1<\xd8G{\x9bEE\xbd\xf4\xe7_\xdf\x96\xb3D\x9f\xe0\xb6',
            "vk": None,
            "sk": b'a\x8a\xb3\x89o\xaf\xc50\xf1$\xe2y\xea\xe1<\xd8G{\x9bEE\xbd\xf4\xe7_\xdf\x96\xb3D\x9f\xe0\xb6)\xc8\x00i \xa6\x9b\xb3\x80Ci\xd1\x96]\x05N*b\x96zzng\x12\xe4\x0eH\xc9:\n\xd6\xe5',
            "did": 'did:dad: KcgAaSCmm7OAQ2nRll0FTipilnp6bmcS5A5IyToK1uU =',
            "valid": False,
            "error": 'Both private and public keys required'
        },
        "10": {
            "seed": b'a\x8a\xb3\x89o\xaf\xc50\xf1$\xe2y\xea\xe1<\xd8G{\x9bEE\xbd\xf4\xe7_\xdf\x96\xb3D\x9f\xe0\xb6',
            "vk": b')\xc8\x00i \xa6\x9b\xb3\x80Ci\xd1\x96]\x05N*b\x96zzng\x12\xe4\x0eH\xc9:\n\xd6\xe5',
            "sk": None,
            "did": 'did:dad: KcgAaSCmm7OAQ2nRll0FTipilnp6bmcS5A5IyToK1uU =',
            "valid": False,
            "error": 'Both private and public keys required'
        },
        "11": {
            "seed": None,
            "vk": b')\xc8\x00i \xa6\x9b\xb3\x80Ci\xd1\x96]\x05N*b\x96zzng\x12\xe4\x0eH\xc9:\n\xd6\xe5',
            "sk": None,
            "did": 'did:dad: KcgAaSCmm7OAQ2nRll0FTipilnp6bmcS5A5IyToK1uU =',
            "valid": False,
            "error": 'Both private and public keys required'
        },
        "12": {
            "seed": None,
            "vk": b')\xc8\x00i \xa6\x9b\xb3\x80Ci\xd1\x96]\x05N*b\x96zzng\x12\xe4\x0eH\xc9:\n\xd6\xe5',
            "sk": b'a\x8a\xb3\x89o\xaf\xc50\xf1$\xe2y\xea\xe1<\xd8G{\x9bEE\xbd\xf4\xe7_\xdf\x96\xb3D\x9f\xe0\xb6)\xc8\x00i \xa6\x9b\xb3\x80Ci\xd1\x96]\x05N*b\x96zzng\x12\xe4\x0eH\xc9:\n\xd6\xe5',
            "did": None,
            "valid": True
        },
        "13": {
            "seed": b'a\x8a\xb3\x89o\xaf\xc50\xf1$\xe2y\xea\xe1<\xd8G{\x9bEE\xbd\xf4\xe7_\xdf\x96\xb3D\x9f\xe0\xb6',
            "vk": None,
            "sk": b'a\x8a\xb3\x89o\xaf\xc50\xf1$\xe2y\xea\xe1<\xd8G{\x9bEE\xbd\xf4\xe7_\xdf\x96\xb3D\x9f\xe0\xb6)\xc8\x00i \xa6\x9b\xb3\x80Ci\xd1\x96]\x05N*b\x96zzng\x12\xe4\x0eH\xc9:\n\xd6\xe5',
            "did": None,
            "valid": False,
            "error": 'Both private and public keys required'
        },
        "14": {
            "seed": b'a\x8a\xb3\x89o\xaf\xc50\xf1$\xe2y\xea\xe1<\xd8G{\x9bEE\xbd\xf4\xe7_\xdf\x96\xb3D\x9f\xe0\xb6',
            "vk": None,
            "sk": None,
            "did": 'did:dad: KcgAaSCmm7OAQ2nRll0FTipilnp6bmcS5A5IyToK1uU =',
            "valid": False,
            "error": 'Keys required with did'
        },
        "15": {
            "seed": None,
            "vk": None,
            "sk": b'a\x8a\xb3\x89o\xaf\xc50\xf1$\xe2y\xea\xe1<\xd8G{\x9bEE\xbd\xf4\xe7_\xdf\x96\xb3D\x9f\xe0\xb6)\xc8\x00i \xa6\x9b\xb3\x80Ci\xd1\x96]\x05N*b\x96zzng\x12\xe4\x0eH\xc9:\n\xd6\xe5',
            "did": None,
            "valid": False,
            "error": 'Both private and public keys required'
        },
        "16": {
            "seed": None,
            "vk": b')\xc8\x00i \xa6\x9b\xb3\x80Ci\xd1\x96]\x05N*b\x96zzng\x12\xe4\x0eH\xc9:\n\xd6\xe5',
            "sk": None,
            "did": None,
            "valid": False,
            "error": 'Both private and public keys required'
        },
        "17": {
            "seed": b'a\x8a\xb3\x89o\xaf\xc50\xf1$\xe2y\xea\xe1<\xd8G{\x9bEE\xbd\xf4\xe7_\xdf\x96\xb3D\x9f\xe0\xb6',
            "vk": b')\xc8\x00i \xa6\x9b\xb3\x80Ci\xd1\x96]\x05N*b\x96zzng\x12\xe4\x0eH\xc9:\n\xd6',
            "sk": b'a\x8a\xb3\x89o\xaf\xc50\xf1$\xe2y\xea\xe1<\xd8G{\x9bEE\xbd\xf4\xe7_\xdf\x96\xb3D\x9f\xe0\xb6)\xc8\x00i \xa6\x9b\xb3\x80Ci\xd1\x96]\x05N*b\x96zzng\x12\xe4\x0eH\xc9:\n\xd6\xe5',
            "did": 'did:dad: KcgAaSCmm7OAQ2nRll0FTipilnp6bmcS5A5IyToK1uU =',
            "valid": False,
            "error": 'Invalid key'
        },
        "18": {
            "seed": b'a\x8a\xb3\x89o\xaf\xc50\xf1$\xe2y\xea\xe1<\xd8G{\x9bEE\xbd\xf4\xe7_\xdf\x96\xb3D\x9f\xe0\xb6',
            "vk": b')\xc8\x00i \xa6\x9b\xb3\x80Ci\xd1\x96]\x05N*b\x96zzng\x12\xe4\x0eH\xc9:\n\xd6\xe5',
            "sk": b'a\x8a\xb3\x89o\xaf\xc50\xf1$\xe2y\xea\xe1<\xd8G{\x9bEE\xbd\xf4\xe7_\xdf\x96\xb3D\x9f\xe0\xb6)\xc8\x00i \xa6\x9b\xb3\x80Ci\xd1\x96]\x05N*b\x96zzng\x12\xe4\x0eH\xc9:\n\xd6',
            "did": 'did:dad: KcgAaSCmm7OAQ2nRll0FTipilnp6bmcS5A5IyToK1uU =',
            "valid": False,
            "error": 'Invalid key'
        }
    }

    for i, data in permutations.items():
        if data["valid"]:
            assert gen.DidBox(data["seed"], data["sk"], data["vk"], data["did"])
        else:
            with pytest.raises(ValueError, message=data["error"]):
                gen.DidBox(data["seed"], data["sk"], data["vk"], data["did"])


def testDidBoxHex_vk():
    data = {
        "seed": b'a\x8a\xb3\x89o\xaf\xc50\xf1$\xe2y\xea\xe1<\xd8G{\x9bEE\xbd\xf4\xe7_\xdf\x96\xb3D\x9f\xe0\xb6',
        "vk": b')\xc8\x00i \xa6\x9b\xb3\x80Ci\xd1\x96]\x05N*b\x96zzng\x12\xe4\x0eH\xc9:\n\xd6\xe5',
        "sk": b'a\x8a\xb3\x89o\xaf\xc50\xf1$\xe2y\xea\xe1<\xd8G{\x9bEE\xbd\xf4\xe7_\xdf\x96\xb3D\x9f\xe0\xb6)\xc8\x00i \xa6\x9b\xb3\x80Ci\xd1\x96]\x05N*b\x96zzng\x12\xe4\x0eH\xc9:\n\xd6\xe5',
        "did": 'did:dad: KcgAaSCmm7OAQ2nRll0FTipilnp6bmcS5A5IyToK1uU ='
    }

    didBox = gen.DidBox(data["seed"], data["sk"], data["vk"], data["did"])

    assert b'29c8006920a69bb3804369d1965d054e2a62967a7a6e6712e40e48c93a0ad6e5' == didBox.hex_vk()


def testDidBoxHex_sk():
    data = {
        "seed": b'a\x8a\xb3\x89o\xaf\xc50\xf1$\xe2y\xea\xe1<\xd8G{\x9bEE\xbd\xf4\xe7_\xdf\x96\xb3D\x9f\xe0\xb6',
        "vk": b')\xc8\x00i \xa6\x9b\xb3\x80Ci\xd1\x96]\x05N*b\x96zzng\x12\xe4\x0eH\xc9:\n\xd6\xe5',
        "sk": b'a\x8a\xb3\x89o\xaf\xc50\xf1$\xe2y\xea\xe1<\xd8G{\x9bEE\xbd\xf4\xe7_\xdf\x96\xb3D\x9f\xe0\xb6)\xc8\x00i \xa6\x9b\xb3\x80Ci\xd1\x96]\x05N*b\x96zzng\x12\xe4\x0eH\xc9:\n\xd6\xe5',
        "did": 'did:dad: KcgAaSCmm7OAQ2nRll0FTipilnp6bmcS5A5IyToK1uU ='
    }

    didBox = gen.DidBox(data["seed"], data["sk"], data["vk"], data["did"])
    hex_sk = b'618ab3896fafc530f124e279eae13cd8477b9b4545bdf4e75fdf96b3449fe0b629c8006920a69bb' \
             b'3804369d1965d054e2a62967a7a6e6712e40e48c93a0ad6e5'

    assert hex_sk == didBox.hex_sk()


def testDidBoxHex_seed():
    data = {
        "seed": b'a\x8a\xb3\x89o\xaf\xc50\xf1$\xe2y\xea\xe1<\xd8G{\x9bEE\xbd\xf4\xe7_\xdf\x96\xb3D\x9f\xe0\xb6',
        "vk": b')\xc8\x00i \xa6\x9b\xb3\x80Ci\xd1\x96]\x05N*b\x96zzng\x12\xe4\x0eH\xc9:\n\xd6\xe5',
        "sk": b'a\x8a\xb3\x89o\xaf\xc50\xf1$\xe2y\xea\xe1<\xd8G{\x9bEE\xbd\xf4\xe7_\xdf\x96\xb3D\x9f\xe0\xb6)\xc8\x00i \xa6\x9b\xb3\x80Ci\xd1\x96]\x05N*b\x96zzng\x12\xe4\x0eH\xc9:\n\xd6\xe5',
        "did": 'did:dad: KcgAaSCmm7OAQ2nRll0FTipilnp6bmcS5A5IyToK1uU ='
    }

    didBox = gen.DidBox(data["seed"], data["sk"], data["vk"], data["did"])
    hex_seed = b'618ab3896fafc530f124e279eae13cd8477b9b4545bdf4e75fdf96b3449fe0b6'

    assert hex_seed == didBox.hex_seed()


def testDidBoxBase64_vk():
    data = {
        "seed": b'a\x8a\xb3\x89o\xaf\xc50\xf1$\xe2y\xea\xe1<\xd8G{\x9bEE\xbd\xf4\xe7_\xdf\x96\xb3D\x9f\xe0\xb6',
        "vk": b')\xc8\x00i \xa6\x9b\xb3\x80Ci\xd1\x96]\x05N*b\x96zzng\x12\xe4\x0eH\xc9:\n\xd6\xe5',
        "sk": b'a\x8a\xb3\x89o\xaf\xc50\xf1$\xe2y\xea\xe1<\xd8G{\x9bEE\xbd\xf4\xe7_\xdf\x96\xb3D\x9f\xe0\xb6)\xc8\x00i \xa6\x9b\xb3\x80Ci\xd1\x96]\x05N*b\x96zzng\x12\xe4\x0eH\xc9:\n\xd6\xe5',
        "did": 'did:dad: KcgAaSCmm7OAQ2nRll0FTipilnp6bmcS5A5IyToK1uU ='
    }

    didBox = gen.DidBox(data["seed"], data["sk"], data["vk"], data["did"])
    base64_vk = 'KcgAaSCmm7OAQ2nRll0FTipilnp6bmcS5A5IyToK1uU='

    assert base64_vk == didBox.base64_vk()


def testDidBoxBase64_sk():
    data = {
        "seed": b'a\x8a\xb3\x89o\xaf\xc50\xf1$\xe2y\xea\xe1<\xd8G{\x9bEE\xbd\xf4\xe7_\xdf\x96\xb3D\x9f\xe0\xb6',
        "vk": b')\xc8\x00i \xa6\x9b\xb3\x80Ci\xd1\x96]\x05N*b\x96zzng\x12\xe4\x0eH\xc9:\n\xd6\xe5',
        "sk": b'a\x8a\xb3\x89o\xaf\xc50\xf1$\xe2y\xea\xe1<\xd8G{\x9bEE\xbd\xf4\xe7_\xdf\x96\xb3D\x9f\xe0\xb6)\xc8\x00i \xa6\x9b\xb3\x80Ci\xd1\x96]\x05N*b\x96zzng\x12\xe4\x0eH\xc9:\n\xd6\xe5',
        "did": 'did:dad: KcgAaSCmm7OAQ2nRll0FTipilnp6bmcS5A5IyToK1uU ='
    }

    didBox = gen.DidBox(data["seed"], data["sk"], data["vk"], data["did"])
    base64_sk = 'YYqziW-vxTDxJOJ56uE82Ed7m0VFvfTnX9-Ws0Sf4LYpyABpIKabs4BDadGWXQVOKmKWenpuZxLkDkjJOgrW5Q=='

    assert base64_sk == didBox.base64_sk()


def testDidBoxBase64_seed():
    data = {
        "seed": b'a\x8a\xb3\x89o\xaf\xc50\xf1$\xe2y\xea\xe1<\xd8G{\x9bEE\xbd\xf4\xe7_\xdf\x96\xb3D\x9f\xe0\xb6',
        "vk": b')\xc8\x00i \xa6\x9b\xb3\x80Ci\xd1\x96]\x05N*b\x96zzng\x12\xe4\x0eH\xc9:\n\xd6\xe5',
        "sk": b'a\x8a\xb3\x89o\xaf\xc50\xf1$\xe2y\xea\xe1<\xd8G{\x9bEE\xbd\xf4\xe7_\xdf\x96\xb3D\x9f\xe0\xb6)\xc8\x00i \xa6\x9b\xb3\x80Ci\xd1\x96]\x05N*b\x96zzng\x12\xe4\x0eH\xc9:\n\xd6\xe5',
        "did": 'did:dad: KcgAaSCmm7OAQ2nRll0FTipilnp6bmcS5A5IyToK1uU ='
    }

    didBox = gen.DidBox(data["seed"], data["sk"], data["vk"], data["did"])
    base64_seed = 'YYqziW-vxTDxJOJ56uE82Ed7m0VFvfTnX9-Ws0Sf4LY='

    assert base64_seed == didBox.base64_seed()


def testDidBoxFor_json():
    data = {
        "seed": b'a\x8a\xb3\x89o\xaf\xc50\xf1$\xe2y\xea\xe1<\xd8G{\x9bEE\xbd\xf4\xe7_\xdf\x96\xb3D\x9f\xe0\xb6',
        "vk": b')\xc8\x00i \xa6\x9b\xb3\x80Ci\xd1\x96]\x05N*b\x96zzng\x12\xe4\x0eH\xc9:\n\xd6\xe5',
        "sk": b'a\x8a\xb3\x89o\xaf\xc50\xf1$\xe2y\xea\xe1<\xd8G{\x9bEE\xbd\xf4\xe7_\xdf\x96\xb3D\x9f\xe0\xb6)\xc8\x00i \xa6\x9b\xb3\x80Ci\xd1\x96]\x05N*b\x96zzng\x12\xe4\x0eH\xc9:\n\xd6\xe5',
        "did": 'did:dad: KcgAaSCmm7OAQ2nRll0FTipilnp6bmcS5A5IyToK1uU ='
    }

    didBox = gen.DidBox(data["seed"], data["sk"], data["vk"], data["did"])
    exp = {
        "priv": b'618ab3896fafc530f124e279eae13cd8477b9b4545bdf4e75fdf96b3449fe0b629c8006920a69bb3804369d1965d054e2a62967a7a6e6712e40e48c93a0ad6e5'.decode(),
        "verify": b'29c8006920a69bb3804369d1965d054e2a62967a7a6e6712e40e48c93a0ad6e5'.decode(),
        "sign": b'618ab3896fafc530f124e279eae13cd8477b9b4545bdf4e75fdf96b3449fe0b6'.decode()
    }

    assert exp == didBox.for_json()


def testDidBoxFor_json64():
    data = {
        "seed": b'a\x8a\xb3\x89o\xaf\xc50\xf1$\xe2y\xea\xe1<\xd8G{\x9bEE\xbd\xf4\xe7_\xdf\x96\xb3D\x9f\xe0\xb6',
        "vk": b')\xc8\x00i \xa6\x9b\xb3\x80Ci\xd1\x96]\x05N*b\x96zzng\x12\xe4\x0eH\xc9:\n\xd6\xe5',
        "sk": b'a\x8a\xb3\x89o\xaf\xc50\xf1$\xe2y\xea\xe1<\xd8G{\x9bEE\xbd\xf4\xe7_\xdf\x96\xb3D\x9f\xe0\xb6)\xc8\x00i \xa6\x9b\xb3\x80Ci\xd1\x96]\x05N*b\x96zzng\x12\xe4\x0eH\xc9:\n\xd6\xe5',
        "did": 'did:dad: KcgAaSCmm7OAQ2nRll0FTipilnp6bmcS5A5IyToK1uU ='
    }

    didBox = gen.DidBox(data["seed"], data["sk"], data["vk"], data["did"])
    exp = {
        "priv": 'YYqziW-vxTDxJOJ56uE82Ed7m0VFvfTnX9-Ws0Sf4LYpyABpIKabs4BDadGWXQVOKmKWenpuZxLkDkjJOgrW5Q==',
        "verify": 'KcgAaSCmm7OAQ2nRll0FTipilnp6bmcS5A5IyToK1uU=',
        "sign": 'YYqziW-vxTDxJOJ56uE82Ed7m0VFvfTnX9-Ws0Sf4LY='
    }

    assert exp == didBox.for_json64()


def testDidBoxNoParams():
    didBox = gen.DidBox()

    assert didBox.seed is not None
    assert didBox.vk is not None
    assert didBox.sk is not None
    assert didBox.did is not None


def testDidBoxWithSeed():
    seed = b'a\x8a\xb3\x89o\xaf\xc50\xf1$\xe2y\xea\xe1<\xd8G{\x9bEE\xbd\xf4\xe7_\xdf\x96\xb3D\x9f\xe0\xb6'

    didBox = gen.DidBox(seed=seed)

    assert didBox.seed == seed
    assert didBox.vk is not None
    assert didBox.sk is not None
    assert didBox.did is not None


def testDidBoxWithKeys():
    vk = b')\xc8\x00i \xa6\x9b\xb3\x80Ci\xd1\x96]\x05N*b\x96zzng\x12\xe4\x0eH\xc9:\n\xd6\xe5'
    sk = b'a\x8a\xb3\x89o\xaf\xc50\xf1$\xe2y\xea\xe1<\xd8G{\x9bEE\xbd\xf4\xe7_\xdf\x96\xb3D\x9f\xe0\xb6)\xc8\x00i \xa6\x9b\xb3\x80Ci\xd1\x96]\x05N*b\x96zzng\x12\xe4\x0eH\xc9:\n\xd6\xe5'

    didBox = gen.DidBox(vk=vk, sk=sk)

    assert didBox.seed is None
    assert didBox.vk == vk
    assert didBox.sk == sk
    assert didBox.did is not None
