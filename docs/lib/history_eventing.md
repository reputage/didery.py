# history_eventing.py

This module provides methods for asynchronously polling multiple didery servers for rotation history events.  The methods will automatically check for a 2/3 majority of matching responses from didery servers.

### history_eventing.getHistoryEvents(did, urls)
getHistoryEvents accepts a W3C decentralized identifier([DID](https://w3c-ccg.github.io/did-spec/)) string and a list of urls to poll and returns all events for a rotation history.  This includes the inception event and all subsequent rotations events with their corresponding signatures so you can verify that the data and the current key are all valid. All data returned from the didery servers is put through a consensus algorithm that requires a 2/3 majority of data to match. If 2/3 of the urls returned matching data a single copy of the data is returned.  If a majority consensus cannot be found then None is returned.  The http request results are returned as a dict of key(url) value(status) pairs. 

**did** (_required_)- W3C decentralized identifier([DID](https://w3c-ccg.github.io/did-spec/)) string   
**urls** (_required_)- list of url strings to query

**returns** - (dict, dict) containing the events as shown in the output section below and a results dict containing a short string description for each url. The results dict can be used to determine what urls failed.

#### Example
```python
import diderypy.lib.history_eventing as events
import diderypy.lib.historying as hist
import diderypy.lib.generating as gen

# rotation history must already exist before sending the put request
history, vk, sk, pvk, psk = gen.historyGen()
did = history["id"]

urls = ["http://localhost:8080", "http://localhost:8000"]

hist.postHistory(history, sk, urls)

# generate the new pre rotated key
new_pvk, new_psk, unneeded = gen.keyGen()

# add public key to history
history["signers"].append(new_pvk)

# update current signer
history["signer"] = 1

# send rotation event
hist.putHistory(history,sk, psk, urls)

data, results = events.getHistoryEvents(did, urls)

if data is None:
    # Consensus could not be reached. Print results for each url
    for url, result in results.items():
        print("{}:\t{}".format(url, result))
else:
    print(data)
``` 

#### Output
```json
{
    "events": {
        "1": {
            "history": {
                "id": "did:dad:l8jrnoFp-D1SUYZtrp-McD_L2lVmBdKI1LS3hJ6D0Fc=", 
                "signer": 1, 
                "signers": [
                    "l8jrnoFp-D1SUYZtrp-McD_L2lVmBdKI1LS3hJ6D0Fc=", 
                    "HOTSwhtdXXPBYiqtzVz2yGUzipFPjuAuEALbe0FFwzc=", 
                    "KSAHDoapdn1SW2WVbqlRac3UqJp7tgMRPdjtUEx8Drw="
                ], 
                "changed": "2018-09-04T22:39:32.512473+00:00"
            }, 
            "signatures": {
                "signer": "9msgtbfjmCyaOkZgeW-q_N6bGUZGTZ-6z54fAf-juzhXgI0G8QfBk9P_Mzr832AdXjLus1QvOjNj-It_fnsVAw==", 
                "rotation": "x7lA29AXGGDiDxSrPEBO4-hwQg2ILEk0XVvJyUM1OdSWl5agBjmFCch3_L8WtmtIUZGDzYRD3JZpXztISmF0CQ=="
            }
        }, 
        "0": {
            "history": {
                "id": "did:dad:l8jrnoFp-D1SUYZtrp-McD_L2lVmBdKI1LS3hJ6D0Fc=", 
                "signer": 0, 
                "signers": [
                    "l8jrnoFp-D1SUYZtrp-McD_L2lVmBdKI1LS3hJ6D0Fc=", 
                    "HOTSwhtdXXPBYiqtzVz2yGUzipFPjuAuEALbe0FFwzc="
                ], 
                "changed": "2018-09-04T22:39:32.483239+00:00"
            }, 
            "signatures": {
                "signer": "X76g8FU1nxTiJZFpbrLIpGFPMIcpQnQ4dwB7G_AR3ksb1BCVMajzCoe2J4fXfNolOvU7i8kW7m_p6X1ETtWtCQ=="
            }
        }
    }
}
```