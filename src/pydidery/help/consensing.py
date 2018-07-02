try:
    import simplejson as json
except ImportError:
    import json

from .helping import verify64u, validateDid

MAJORITY = 2 / 3
RESPONSE = 0
STATUS = 1


def validateHistorySignatures(data):
    valid_data = {}
    sig_counts = {}
    num_valid = 0

    if not data:
        return None, None

    for datum in data:
        if datum[STATUS] != 200:
            continue

        datum = json.loads(datum[RESPONSE])

        history = datum["history"]
        keyIndex = int(history["signer"])

        vk = history["signers"][keyIndex]
        if "rotation" in datum["signatures"]:
            signature = datum["signatures"]["rotation"]
        else:
            signature = datum["signatures"]["signer"]

        if verify64u(signature, json.dumps(history, ensure_ascii=False, separators=(',', ':')).encode(), vk):
            num_valid += 1
            # keep track of data that belongs to signature
            valid_data[signature] = datum
            # Count number of times the signature has been seen
            sig_counts[signature] = sig_counts.get(signature, 0) + 1

    # check that a majority of signatures are valid
    if len(data) * MAJORITY > num_valid:
        return None, None
    else:
        return valid_data, sig_counts


def validateOtpSignatures(data):
    valid_data = {}
    sig_counts = {}
    num_valid = 0

    if not data:
        return None, None

    for datum in data:
        if datum[STATUS] != 200:
            continue

        datum = json.loads(datum[RESPONSE])

        otp = datum["otp_data"]
        did, vk = validateDid(otp["id"])
        signature = datum["signature"][0]

        if verify64u(signature, json.dumps(otp, ensure_ascii=False, separators=(',', ':')).encode(), vk):
            num_valid += 1
            # keep track of data that belongs to signature
            valid_data[signature] = datum
            # Count number of times the signature has been seen
            sig_counts[signature] = sig_counts.get(signature, 0) + 1

    # check that a majority of signatures are valid
    if len(data) * MAJORITY > num_valid:
        return None, None
    else:
        return valid_data, sig_counts


def consense(data, dtype="history"):
    """
    Validates signatures and data and then checks
    if a majority of the data items are equal by
    comparing their signatures.

    :param data: list of history dicts returned by the didery server
    :param dtype: string specifying to consense otp or history data
    :return: history dict if consensus is reached else None
    """
    if dtype == "history":
        valid_data, sig_counts = validateHistorySignatures(data)
    else:
        valid_data, sig_counts = validateOtpSignatures(data)

    # Not enough valid signatures
    if valid_data is None:
        return None

    # All signatures are equal
    if len(valid_data) == 1:
        return valid_data.popitem()[1]

    for sig, count in sig_counts.items():
        if count >= len(data) * MAJORITY:
            return valid_data[sig]

    return None
