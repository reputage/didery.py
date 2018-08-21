# historying.py

This module provides methods for asynchronously broadcasting and polling multiple didery servers for rotation histories.  In the event of polling from the servers the methods will automatically check for a 2/3 majority of matching responses.


### historying.postHistory(data, sk, urls)
postHistory accepts a didery rotation history, a signing/private key, and a list of urls and returns a dictionary of url, response key pairs

**data** (_required_)- rotation history as specified in the [didery documentation](https://github.com/reputage/didery/wiki/Public-API#add-rotation-history)  
**sk** (_required_)- current signing key. base64 url-file safe signing/private key from EdDSA (Ed25519) key pair  
**urls** (_required_)- list of url strings to query  

#### Example
```python
import pydidery.lib.historying as hist
import pydidery.lib.generating as gen

# generate the rotation history
history, vk, sk, pvk, psk = gen.historyGen()

urls = ["http://localhost:8080", "http://localhost:8000"]

result = hist.postHistory(history, sk, urls)

print(result)
```

#### Output
```
{
    'http://localhost:8000': (
        {
            "history": {
                "id": "did:dad:cF8UIyTkUYg-I0kW5VmOsvy69Usmwy4-VgNxaeM95W8=", 
                "signer": 0, 
                "signers": [
                    "cF8UIyTkUYg-I0kW5VmOsvy69Usmwy4-VgNxaeM95W8=", 
                    "sPCgHd2yrudecNchcXXCHVybFr9HfXPIcTP0xddJBNY="
                ], 
                "changed": "2018-07-16T19:52:39.115677+00:00"
            }, 
            "signatures": {
                "signer": "7J2kDoAd975cDwdczE6H-9HBqVPHl4mvQepsO1nhe1eH9rLZsHzv7Bd9uufmWGKEKbowMQROONSIiROMam7CDQ=="
            }
        }, 
        201
    ), 
    'http://localhost:8080': (
        {
            "history": {
                "id": "did:dad:cF8UIyTkUYg-I0kW5VmOsvy69Usmwy4-VgNxaeM95W8=", 
                "signer": 0, 
                "signers": [
                    "cF8UIyTkUYg-I0kW5VmOsvy69Usmwy4-VgNxaeM95W8=", 
                    "sPCgHd2yrudecNchcXXCHVybFr9HfXPIcTP0xddJBNY="
                ], 
                "changed": "2018-07-16T19:52:39.115677+00:00"
            }, 
            "signatures": {
                "signer": "7J2kDoAd975cDwdczE6H-9HBqVPHl4mvQepsO1nhe1eH9rLZsHzv7Bd9uufmWGKEKbowMQROONSIiROMam7CDQ=="
            }
        },
        201
    )
}
```

### historying.putHistory(data, sk, psk, urls)
putHistory sends a rotation event to the didery servers where they verify and store the event. putHistory returns a dictionary of url, response key pairs

**data** (_required_)- rotation history as specified in the [didery documentation](https://github.com/reputage/didery/wiki/Public-API#rotation-event)  
**sk** (_required_)- current signing key. base64 url-file safe signing/private key from EdDSA (Ed25519) key pair  
**psk** (_required_)- pre rotated signing key. base64 url-file safe signing/private key from EdDSA (Ed25519) key pair  
**urls** (_required_)- list of url strings to query  

#### Example
```python
import pydidery.lib.historying as hist
import pydidery.lib.generating as gen

# rotation history must already exist before sending the put request
history, vk, sk, pvk, psk = gen.historyGen()

urls = ["http://localhost:8080", "http://localhost:8000"]

hist.postHistory(history, sk, urls)

# generate the new pre rotated key
new_pvk, new_psk = gen.keyGen()

# add public key to history
history["signers"].append(new_pvk)

# update current signer
history["signer"] = 1

# send rotation event
result = hist.putHistory(history,sk, psk, urls)

print(result)
```

#### Output
```
{
    'http://localhost:8000': (
        {
            'history': {
                'id': 'did:dad:R_B11yIRNt19ty_Lvt8OpZuA0_Mgs1he6zPXyttl4V4=', 
                'signer': 1, 
                'signers': [
                    'R_B11yIRNt19ty_Lvt8OpZuA0_Mgs1he6zPXyttl4V4=', 
                    'Qbf97bKWC2G5KYM0BSX4aMWiLx-Exh3FUf4E7k6i_AY=', 
                    'DHowCo3BOUyxXfx9LhI9koSDI7IQwiM7aV4H7AZ6I_A='
                ], 
                'changed': '2018-07-16T20:18:29.527613+00:00'
            }, 
            'signatures': {
                'signer': 'edDONPBidBWn1gQWNIRjtKeURGAKlfH5aHm-Ib_9thqJfVAlqaS4wSl8Ru_nHNU04OEgO9-FtvxQq_NXxyGmBQ==', 
                'rotation': '6hsvAoZmwzqZxegm6JeYpuFPTVQIL2g0NAiF-tkDdhnVBnMp2I5XC4iC7FPqsCbosTcl0Ddnaj8LkVKIzgTdCA=='
            }
        }, 
        200
    ), 
    'http://localhost:8080': (
        {
            'history': {
                'id': 'did:dad:R_B11yIRNt19ty_Lvt8OpZuA0_Mgs1he6zPXyttl4V4=', 
                'signer': 1, 
                'signers': [
                    'R_B11yIRNt19ty_Lvt8OpZuA0_Mgs1he6zPXyttl4V4=', 
                    'Qbf97bKWC2G5KYM0BSX4aMWiLx-Exh3FUf4E7k6i_AY=', 
                    'DHowCo3BOUyxXfx9LhI9koSDI7IQwiM7aV4H7AZ6I_A='
                ], 
                'changed': '2018-07-16T20:18:29.527613+00:00'
            }, 
            'signatures': {
                'signer': 'edDONPBidBWn1gQWNIRjtKeURGAKlfH5aHm-Ib_9thqJfVAlqaS4wSl8Ru_nHNU04OEgO9-FtvxQq_NXxyGmBQ==', 
                'rotation': '6hsvAoZmwzqZxegm6JeYpuFPTVQIL2g0NAiF-tkDdhnVBnMp2I5XC4iC7FPqsCbosTcl0Ddnaj8LkVKIzgTdCA=='
            }
        }, 
        200
    )
}
```

### historying.getHistory(did, urls)
getHistory accepts a W3C decentralized identifier([DID](https://w3c-ccg.github.io/did-spec/)) string and a list of urls to poll and returns a single rotation history if 2/3 of the urls returned matching data.  If less than 2/3 returned matching data None is returned.

**did** (_required_)- W3C decentralized identifier([DID](https://w3c-ccg.github.io/did-spec/)) string   
**urls** (_required_)- list of url strings to query

**returns** - (dict, dict) containing the rotation history as shown on the didery documentation and a results dict containing a short string description for each url. The results dict can be used to determine what urls failed.

#### Example
```python
import pydidery.lib.historying as hist
import pydidery.lib.generating as gen

# generate the rotation history
history, vk, sk, pvk, psk = gen.historyGen()

urls = ["http://localhost:8080", "http://localhost:8000"]

# history must already exist to use getHistory
hist.postHistory(history, sk, urls)

did = history["id"]

data, results = hist.getHistory(did, urls)

if data is None:
    # Consensus could not be reached. Print results for each url
    for url, result in results.items():
        print("{}:\t{}".format(url, result.description()))
else:
    print(data)
``` 

#### Output
```
{
    'history': {
        'id': 'did:dad:g3Jr_qvnh4EERpl0ohu8HNz07gw4Im666Gz7KL81U5g=', 
        'signer': 0, 
        'signers': [
            'g3Jr_qvnh4EERpl0ohu8HNz07gw4Im666Gz7KL81U5g=', 
            'M4t0cFPqWzg6uy2OjOZwhyNQ6rrZBO4DIO51o-Ax7wo='
        ], 
        'changed': '2018-07-16T21:03:41.381008+00:00'
    }, 
    'signatures': {
        'signer': 'TnC14l6ojngaVfmRJLqePT4YC22wgKgAd7GFDlyWswshC3G46_FNcMo4rSQxm-tIFgC2VWRXQt_C6wd_HO2qDQ=='
    }
}
```

### historying.deleteHistory(did, sk, urls)
For GDPR compliance a delete method is provided.  For security reasons the data cannot be deleted without signing with the current key. 

**did** (_required_)- W3C decentralized identifier([DID](https://w3c-ccg.github.io/did-spec/)) string
**sk** (_required_)- current signing key. base64 url-file safe signing/private key from EdDSA (Ed25519) key pair    
**urls** (_required_)- list of url strings to query   

**returns** - dict containing the rotation history that was deleted.

#### Example
```python
import pydidery.lib.historying as hist
import pydidery.lib.generating as gen

# generate the rotation history
history, vk, sk, pvk, psk = gen.historyGen()

urls = ["http://localhost:8080", "http://localhost:8000"]

# history must already exist to use getHistory
hist.postHistory(history, sk, urls)

did = history["id"]

response = hist.deleteHistory(did, sk, urls)

print(response)
```  

#### Output
```
{
    "http://localhost:8000": (
        {
            "deleted": {
                "history": {
                    "id": "did:dad:52AeBKEjEOymE4hk6prLgjDhIejh-cIrrnguEaN9-f4=", 
                    "signer": 0, 
                    "signers": [
                      "52AeBKEjEOymE4hk6prLgjDhIejh-cIrrnguEaN9-f4=", 
                      "R0H-ew626o3i1bZy1D4E_lhTY3A7HFi0nrlUWfgcvVc="
                    ], 
                    "changed": "2018-08-01T23:46:49.730952+00:00"
                }, 
                "signatures": {
                    "signer": "pUMUiSMYs1xG62MmvcNGDnOlxuIGeUL1FsMklIhvDiaYbRfDKnSW8exfcVzOia9m0Hn7yi7kib2qq35FP4rPCQ=="
                }
            }
        }, 
        200
    ), 
    "http://localhost:8080": (
        {
            "deleted": {
                "history": {
                    "id": "did:dad:52AeBKEjEOymE4hk6prLgjDhIejh-cIrrnguEaN9-f4=", 
                    "signer": 0, 
                    "signers": [
                        "52AeBKEjEOymE4hk6prLgjDhIejh-cIrrnguEaN9-f4=", 
                        "R0H-ew626o3i1bZy1D4E_lhTY3A7HFi0nrlUWfgcvVc="
                    ], 
                    "changed": "2018-08-01T23:46:49.730952+00:00"
                }, 
                "signatures": {
                    "signer": "pUMUiSMYs1xG62MmvcNGDnOlxuIGeUL1FsMklIhvDiaYbRfDKnSW8exfcVzOia9m0Hn7yi7kib2qq35FP4rPCQ=="
                }
            }
        }, 
        200
    )
}
```