from diderypy.help import consensing
from tests.data import history_data_builder as builder


HISTORY = 0
VK1 = 1
SK1 = 2
VK2 = 3
SK2 = 4


def testValidateDataInvalidSigsIncompleteMajority():
    consense = consensing.Consense()

    response1 = builder.DideryResponseBuilder(
        builder.SignedHistoryBuilder().withInvalidSignerSignature()
    ).withPort(8000)
    response2 = builder.DideryResponseBuilder(
        builder.SignedHistoryBuilder()
    )

    data = {
        "http://localhost:8000/history": response1.build(),
        "http://localhost:8080/history": response2.build()
    }

    consense.validateData(data)

    history2 = response2.historyBuilder
    assert consense.valid_data == {
        history2.signerSig: builder.SignedHistoryBuilder().build().data
    }
    assert consense.valid_match_counts == {
        history2.signerSig: 1
    }


def testValidateDataEmptyData():
    consense = consensing.Consense()
    consense.validateData({})

    assert consense.valid_data == {}
    assert consense.valid_match_counts == {}


def testValidateDataMajorityPasses():
    consense = consensing.Consense()
    response1 = builder.DideryResponseBuilder(
        builder.SignedHistoryBuilder().withInvalidSignerSignature()
    ).withPort(8000)
    response2 = builder.DideryResponseBuilder(
        builder.SignedHistoryBuilder()
    )
    response3 = builder.DideryResponseBuilder(
        builder.SignedHistoryBuilder()
    ).withPort(8081)

    data = {
        "http://localhost:8000/history": response1.build(),
        "http://localhost:8080/history": response2.build(),
        "http://localhost:8081/history": response3.build()
    }

    consense.validateData(data)

    history2 = response2.historyBuilder

    assert consense.valid_data == {
        history2.signerSig: builder.SignedHistoryBuilder().build().data
    }
    assert history2.signerSig in consense.valid_match_counts
    assert consense.valid_match_counts[history2.signerSig] == 2


def testValidateDataMultiSigData():
    consense = consensing.Consense()

    response1 = builder.DideryResponseBuilder(
        builder.SignedHistoryBuilder().withRotation()
    ).withPort(8000)
    response2 = builder.DideryResponseBuilder(
        builder.SignedHistoryBuilder().withRotation()
    )
    response3 = builder.DideryResponseBuilder(
        builder.SignedHistoryBuilder().withInvalidSignerSignature()
    ).withPort(8081)

    data = {
        "http://localhost:8000/history": response1.build(),
        "http://localhost:8080/history": response2.build(),
        "http://localhost:8081/history": response3.build()
    }

    consense.validateData(data)

    history1 = response1.historyBuilder
    assert consense.valid_data == {
        history1.rotationSig: history1.build().data
    }
    assert history1.rotationSig in consense.valid_match_counts
    assert consense.valid_match_counts[history1.rotationSig] == 2


def testValidateDataValidSigsConflictingData():
    consense = consensing.Consense()

    response1 = builder.DideryResponseBuilder(
        builder.SignedHistoryBuilder()
    ).withPort(8000)
    response2 = builder.DideryResponseBuilder(
        builder.SignedHistoryBuilder()
    )
    response3 = builder.DideryResponseBuilder(
        builder.SignedHistoryBuilder().withRotation().withRotation()
    ).withPort(8081)

    data = {
        "http://localhost:8000/history": response1.build(),
        "http://localhost:8080/history": response2.build(),
        "http://localhost:8081/history": response3.build()
    }

    consense.validateData(data)

    history1 = response1.historyBuilder
    history3 = response3.historyBuilder

    assert consense.valid_data == {
        history1.signerSig: history1.build().data,
        history3.rotationSig: history3.build().data
    }
    assert history1.signerSig in consense.valid_match_counts
    assert consense.valid_match_counts[history1.signerSig] == 2
    assert history3.rotationSig in consense.valid_match_counts
    assert consense.valid_match_counts[history3.rotationSig] == 1


def testValidateDataIncompleteMajority():
    consense = consensing.Consense()

    response1 = builder.DideryResponseBuilder(
        builder.SignedHistoryBuilder()
    ).withPort(8000)
    response2 = builder.DideryResponseBuilder(
        builder.SignedHistoryBuilder()
    )
    response3 = builder.DideryResponseBuilder(
        builder.SignedHistoryBuilder().withRotation().withRotation()
    ).withPort(8081)
    response4 = builder.DideryResponseBuilder(
        builder.SignedHistoryBuilder().withRotation().withRotation()
    ).withPort(8001)

    data = {
        "http://localhost:8000/history": response1.build(),
        "http://localhost:8080/history": response2.build(),
        "http://localhost:8081/history": response3.build(),
        "http://localhost:8001/history": response4.build()
    }

    consense.validateData(data)

    history1 = response1.historyBuilder
    history3 = response3.historyBuilder

    assert consense.valid_data == {
        history1.signerSig: history1.build().data,
        history3.rotationSig: history3.build().data
    }
    assert history1.signerSig in consense.valid_match_counts
    assert consense.valid_match_counts[history1.signerSig] == 2
    assert history3.rotationSig in consense.valid_match_counts
    assert consense.valid_match_counts[history3.rotationSig] == 2


def testConsense():
    consense = consensing.Consense()

    response1 = builder.DideryResponseBuilder(
        builder.SignedHistoryBuilder().withInvalidSignerSignature()
    ).withPort(8000)
    response2 = builder.DideryResponseBuilder(
        builder.SignedHistoryBuilder().withRotation()
    )
    response3 = builder.DideryResponseBuilder(
        builder.SignedHistoryBuilder().withRotation()
    ).withPort(8081)

    data = {
        "http://localhost:8000/history": response1.build(),
        "http://localhost:8080/history": response2.build(),
        "http://localhost:8081/history": response3.build()
    }

    historyObj = response3.historyBuilder.build()
    assert consense.consense(data)[0] == historyObj.data


def testConsenseIncompleteMajority():
    consense = consensing.Consense()

    response1 = builder.DideryResponseBuilder(
        builder.SignedHistoryBuilder().withInvalidSignerSignature()
    ).withPort(8000)
    response2 = builder.DideryResponseBuilder(
        builder.SignedHistoryBuilder().withRotation()
    )
    response3 = builder.DideryResponseBuilder(
        builder.SignedHistoryBuilder().withRotation().withRotation()
    ).withPort(8081)

    data = {
        "http://localhost:8000/history": response1.build(),
        "http://localhost:8080/history": response2.build(),
        "http://localhost:8081/history": response3.build()
    }

    assert consense.consense(data)[0] is None


def testConsenseAllEqual():
    consense = consensing.Consense()

    response1 = builder.DideryResponseBuilder(
        builder.SignedHistoryBuilder().withRotation()
    ).withPort(8000)

    data = {
        "http://localhost:8000/history": response1.withPort(8000).build(),
        "http://localhost:8080/history": response1.withPort(8080).build(),
        "http://localhost:8081/history": response1.withPort(8081).build()
    }

    signature = response1.historyBuilder.rotationSig

    assert consense.consense(data)[0] == response1.historyBuilder.build().data
    assert signature in consense.valid_data
    assert signature in consense.valid_match_counts
    assert consense.valid_match_counts[signature] == 3


def test50_50Split():
    consense = consensing.Consense()

    response1 = builder.DideryResponseBuilder(
        builder.SignedHistoryBuilder()
    ).withPort(8000)
    response2 = builder.DideryResponseBuilder(
        builder.SignedHistoryBuilder()
    )
    response3 = builder.DideryResponseBuilder(
        builder.SignedHistoryBuilder().withRotation().withRotation()
    ).withPort(8081)
    response4 = builder.DideryResponseBuilder(
        builder.SignedHistoryBuilder().withRotation().withRotation()
    ).withPort(8001)

    data = {
        "http://localhost:8000/history": response1.build(),
        "http://localhost:8080/history": response2.build(),
        "http://localhost:8081/history": response3.build(),
        "http://localhost:8001/history": response4.build()
    }

    assert consense.consense(data)[0] is None


def testValidateDataWithHTTPError():
    consense = consensing.Consense()

    response1 = builder.DideryResponseBuilder(
        builder.SignedHistoryBuilder().withEmptyData()
    ).withPort(8000).withStatus(400)
    response2 = builder.DideryResponseBuilder(
        builder.SignedHistoryBuilder()
    )

    data = {
        "http://localhost:8000/history": response1.build(),
        "http://localhost:8080/history": response2.build()
    }

    consense.validateData(data)

    history2 = response2.historyBuilder

    assert consense.valid_data == {
        history2.signerSig: history2.build().data
    }
    assert consense.valid_match_counts == {
        history2.signerSig: 1
    }


def testValidateDataWithTimeOut():
    consense = consensing.Consense()

    response1 = builder.DideryResponseBuilder(
        builder.SignedHistoryBuilder().withEmptyData()
    ).withPort(8000).withStatus(0)
    response2 = builder.DideryResponseBuilder(
        builder.SignedHistoryBuilder()
    )

    data = {
        "http://localhost:8000/history": response1.build(),
        "http://localhost:8080/history": response2.build()
    }

    consense.validateData(data)

    history2 = response2.historyBuilder

    assert consense.valid_data == {
        history2.signerSig: history2.build().data
    }
    assert consense.valid_match_counts == {
        history2.signerSig: 1
    }
