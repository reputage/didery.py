from ..help import helping as h
from ..help import consensing


def __patronHelper(method="GET", path="event", headers=None, data=None):
    result = yield from h.httpRequest(method, path=path, headers=headers, data=data)

    if result:
        return result['body'].decode(), result.get('status')
    else:
        return None


def getHistoryEvents(did, urls):
    consense = consensing.CompositeConsense()
    if not urls:
        raise ValueError("At least one url required.")

    generators = {}

    for url in urls:
        endpoint = "{0}/{1}/{2}".format(url, "event", did)
        generators[endpoint] = __patronHelper(path=endpoint)

    data = h.awaitAsync(generators)
    print(data)
    events, results = consense.consense(data)
    events = {"events": events} if events else events

    return events, results
