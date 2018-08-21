import libnacl

from pydidery.lib import generating as gen


def testDidGen():
    seed = libnacl.randombytes(libnacl.crypto_sign_SEEDBYTES)
    vk, sk = libnacl.crypto_sign_seed_keypair(seed)

    did = gen.didGen(vk)

    assert did == "did:dad:{}".format(gen.keyToKey64u(vk))


def testDidGen64():
    vk, sk = gen.keyGen()

    did = gen.didGen64(vk)

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
    vk, sk = gen.keyGen()

    assert vk
    assert sk


def testKeyGenWithSeed():
    seed = b'\x8dh\xf3\xa0!\xd1\xcd\xc0b\x8c^\x1d\xbcg>\xe1S\x12\xc7\xcb\xbc\x0eTOz@\xdb} \xba\x06\x04'

    vk, sk = gen.keyGen(seed)

    exp_vk = "u8TWIE28yAdu-lGrPHH2ZJ73GxoMBZx-D3cf6RMEaTc="
    exp_sk = "jWjzoCHRzcBijF4dvGc-4VMSx8u8DlRPekDbfSC6BgS7xNYgTbzIB276Uas8cfZknvcbGgwFnH4Pdx_pEwRpNw=="

    assert vk == exp_vk
    assert sk == exp_sk


def testSignResource():
    vk = b'\xbb\xc4\xd6 M\xbc\xc8\x07n\xfaQ\xab<q\xf6d\x9e\xf7\x1b\x1a\x0c\x05\x9c~\x0fw\x1f\xe9\x13\x04i7'
    sk = b'\x8dh\xf3\xa0!\xd1\xcd\xc0b\x8c^\x1d\xbcg>\xe1S\x12\xc7\xcb\xbc\x0eTOz@\xdb} \xba\x06\x04\xbb\xc4\xd6 M\xbc\xc8\x07n\xfaQ\xab<q\xf6d\x9e\xf7\x1b\x1a\x0c\x05\x9c~\x0fw\x1f\xe9\x13\x04i7'
    resource = b'{"data":"TEST!"}'

    signature = gen.signResource(resource, sk)

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
    seed = b'\x8dh\xf3\xa0!\xd1\xcd\xc0b\x8c^\x1d\xbcg>\xe1S\x12\xc7\xcb\xbc\x0eTOz@\xdb} \xba\x06\x04'

    history = gen.historyGen(seed)

    exp_history = ({'id': 'did:dad:u8TWIE28yAdu-lGrPHH2ZJ73GxoMBZx-D3cf6RMEaTc=', 'signer': 0, 'signers': ['u8TWIE28yAdu-lGrPHH2ZJ73GxoMBZx-D3cf6RMEaTc=', 'u8TWIE28yAdu-lGrPHH2ZJ73GxoMBZx-D3cf6RMEaTc=']}, 'u8TWIE28yAdu-lGrPHH2ZJ73GxoMBZx-D3cf6RMEaTc=', 'jWjzoCHRzcBijF4dvGc-4VMSx8u8DlRPekDbfSC6BgS7xNYgTbzIB276Uas8cfZknvcbGgwFnH4Pdx_pEwRpNw==', 'u8TWIE28yAdu-lGrPHH2ZJ73GxoMBZx-D3cf6RMEaTc=', 'jWjzoCHRzcBijF4dvGc-4VMSx8u8DlRPekDbfSC6BgS7xNYgTbzIB276Uas8cfZknvcbGgwFnH4Pdx_pEwRpNw==')

    assert history == exp_history
