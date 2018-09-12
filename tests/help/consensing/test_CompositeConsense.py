from hashlib import sha256
from collections import OrderedDict as ODict

from pydidery.help import consensing
from tests.data import history_data_builder as builder


HISTORY = 0
VK1 = 1
SK1 = 2
VK2 = 3
SK2 = 4


def testValidateDataInvalidSigsIncompleteMajority():
    consense = consensing.CompositeConsense()

    response1 = builder.DideryResponseBuilder(
        builder.CompositeHistoryBuilder().withRotations()
    ).withPort(8000)
    response2 = builder.DideryResponseBuilder(
        builder.CompositeHistoryBuilder().withRotations().withInvalidRotationSigAt(1)
    )

    data = {
        'http://localhost:8000/event/': response1.build(),
        'http://localhost:8080/event/': response2.build()
    }

    consense.validateData(data)

    exp_data = response1.historyBuilder.build()
    sha = sha256(str(ODict(exp_data)).encode()).hexdigest()

    assert sha in consense.valid_data
    assert consense.valid_data[sha]['0'] == exp_data['0'].data
    assert consense.valid_data[sha]['1'] == exp_data['1'].data
    assert sha in consense.valid_match_counts
    assert consense.valid_match_counts == {
        sha: 1
    }


def testValidateDataEmptyData():
    consense = consensing.CompositeConsense()
    consense.validateData({})

    assert consense.valid_data == {}
    assert consense.valid_match_counts == {}


def testValidateDataMajorityPasses():
    consense = consensing.CompositeConsense()

    response1 = builder.DideryResponseBuilder(
        builder.CompositeHistoryBuilder().withRotations()
    ).withPort(8000)
    response2 = builder.DideryResponseBuilder(
        builder.CompositeHistoryBuilder().withRotations().withInvalidRotationSigAt(1)
    )
    response3 = builder.DideryResponseBuilder(
        builder.CompositeHistoryBuilder().withRotations()
    ).withPort(8081)

    data = {
        'http://localhost:8000/event/': response1.build(),
        'http://localhost:8080/event/': response2.build(),
        'http://localhost:8081/event/': response3.build()
    }

    consense.validateData(data)

    exp_data = response1.historyBuilder.build()
    sha = sha256(str(ODict(exp_data)).encode()).hexdigest()

    assert sha in consense.valid_data
    assert consense.valid_data[sha]['0'] == exp_data['0'].data
    assert consense.valid_data[sha]['1'] == exp_data['1'].data
    assert sha in consense.valid_match_counts
    assert consense.valid_match_counts == {
        sha: 2
    }


def testValidateDataValidSigsConflictingData():
    consense = consensing.CompositeConsense()

    response1 = builder.DideryResponseBuilder(
        builder.CompositeHistoryBuilder().withRotations()
    ).withPort(8000)
    response2 = builder.DideryResponseBuilder(
        builder.CompositeHistoryBuilder().withRotations().withRotations()
    )
    response3 = builder.DideryResponseBuilder(
        builder.CompositeHistoryBuilder().withRotations()
    ).withPort(8081)

    data = {
        'http://localhost:8000/event/': response1.build(),
        'http://localhost:8080/event/': response2.build(),
        'http://localhost:8081/event/': response3.build()
    }

    consense.validateData(data)

    exp_data = response1.historyBuilder.build()
    sha = sha256(str(ODict(exp_data)).encode()).hexdigest()
    bad_exp_data = response2.historyBuilder.build()
    bad_sha = sha256(str(ODict(bad_exp_data)).encode()).hexdigest()

    assert sha in consense.valid_data
    assert consense.valid_data[sha]['0'] == exp_data['0'].data
    assert consense.valid_data[sha]['1'] == exp_data['1'].data
    assert sha in consense.valid_match_counts
    assert consense.valid_match_counts[sha] == 2

    assert bad_sha in consense.valid_data
    assert consense.valid_data[bad_sha]['0'] == bad_exp_data['0'].data
    assert consense.valid_data[bad_sha]['1'] == bad_exp_data['1'].data
    assert consense.valid_data[bad_sha]['2'] == bad_exp_data['2'].data
    assert bad_sha in consense.valid_match_counts
    assert consense.valid_match_counts[bad_sha] == 1


def testValidateDataIncompleteMajority():
    consense = consensing.CompositeConsense()

    response1 = builder.DideryResponseBuilder(
        builder.CompositeHistoryBuilder().withRotations()
    ).withPort(8000)
    response2 = builder.DideryResponseBuilder(
        builder.CompositeHistoryBuilder().withRotations().withRotations()
    )
    response3 = builder.DideryResponseBuilder(
        builder.CompositeHistoryBuilder().withRotations().withRotations()
    ).withPort(8081)
    response4 = builder.DideryResponseBuilder(
        builder.CompositeHistoryBuilder().withRotations()
    ).withPort(8001)

    data = {
        'http://localhost:8000/event/': response1.build(),
        'http://localhost:8080/event/': response2.build(),
        'http://localhost:8081/event/': response3.build(),
        'http://localhost:8001/event/': response4.build()
    }

    consense.validateData(data)

    exp_data = response1.historyBuilder.build()
    sha = sha256(str(ODict(exp_data)).encode()).hexdigest()
    bad_exp_data = response2.historyBuilder.build()
    bad_sha = sha256(str(ODict(bad_exp_data)).encode()).hexdigest()

    assert len(consense.valid_data) == 2

    assert sha in consense.valid_data
    assert consense.valid_data[sha]['0'] == exp_data['0'].data
    assert consense.valid_data[sha]['1'] == exp_data['1'].data
    assert sha in consense.valid_match_counts
    assert consense.valid_match_counts[sha] == 2

    assert bad_sha in consense.valid_data
    assert consense.valid_data[bad_sha]['0'] == bad_exp_data['0'].data
    assert consense.valid_data[bad_sha]['1'] == bad_exp_data['1'].data
    assert consense.valid_data[bad_sha]['2'] == bad_exp_data['2'].data
    assert bad_sha in consense.valid_match_counts
    assert consense.valid_match_counts[bad_sha] == 2


def testValidateDataWithHTTPError():
    consense = consensing.CompositeConsense()

    response1 = builder.DideryResponseBuilder(
        builder.CompositeHistoryBuilder().withRotations()
    ).withPort(8000)
    response2 = builder.DideryResponseBuilder(
        builder.CompositeHistoryBuilder().withEmptyData()
    ).withStatus(400)

    data = {
        'http://localhost:8000/event/': response1.build(),
        'http://localhost:8080/event/': response2.build()
    }

    consense.validateData(data)

    exp_data = response1.historyBuilder.build()
    sha = sha256(str(ODict(exp_data)).encode()).hexdigest()

    assert len(consense.valid_data) == 1
    assert sha in consense.valid_data
    assert consense.valid_data[sha]['0'] == exp_data['0'].data
    assert consense.valid_data[sha]['1'] == exp_data['1'].data
    assert sha in consense.valid_match_counts
    assert consense.valid_match_counts == {
        sha: 1
    }


def testValidateDataWithTimeOut():
    consense = consensing.CompositeConsense()

    response1 = builder.DideryResponseBuilder(
        builder.CompositeHistoryBuilder().withRotations()
    ).withPort(8000)
    response2 = builder.DideryResponseBuilder(
        builder.CompositeHistoryBuilder().withEmptyData()
    ).withStatus(0)

    data = {
        'http://localhost:8000/event/': response1.build(),
        'http://localhost:8080/event/': response2.build()
    }

    consense.validateData(data)

    exp_data = response1.historyBuilder.build()
    sha = sha256(str(ODict(exp_data)).encode()).hexdigest()

    assert len(consense.valid_data) == 1
    assert sha in consense.valid_data
    assert consense.valid_data[sha]['0'] == exp_data['0'].data
    assert consense.valid_data[sha]['1'] == exp_data['1'].data
    assert sha in consense.valid_match_counts
    assert consense.valid_match_counts == {
        sha: 1
    }
