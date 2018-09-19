otping.py
=========

This module provides methods for asynchronously broadcasting and polling
multiple didery servers for one time
pad(\ `otp <https://en.wikipedia.org/wiki/One-time_pad>`__) encrypted
blobs. In the event of polling from the servers the methods will
automatically check for a 2/3 majority of matching responses.

otping.postOtpBlob(data, sk, urls)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

postOtpBlob accepts otp blob dict, a signing/private key, and a list of
urls and returns a dictionary of url, response key pairs

| **data** (*required*)- otp encrypted blob data as specified in the
  `didery
  documentation <https://github.com/reputage/didery/wiki/Public-API#add-otp-encrypted-key>`__
| **sk** (*required*)- signing key associated with the public key in the
  accompanying did. base64 url-file safe signing/private key from EdDSA
  (Ed25519) key pair
| **urls** (*required*)- list of url strings to query

Example
^^^^^^^

.. code:: python

    import diderypy.lib.otping as otp
    import diderypy.lib.generating as gen

    # generate a did for the data
    vk, sk, did = gen.keyGen()

    data = {
        "id": did,
        "blob": "AeYbsHot0pmdWAcgTo5sD8iAuSQAfnH5U6wiIGpVNJQQoYKBYrPPxAoIc1i5SHCIDS8KFFgf8i0tDq8XGizaCgo9yjuKHHNJZFi0QD9K6Vpt6fP0XgXlj8z_4D-7s3CcYmuoWAh6NVtYaf_GWw_2sCrHBAA2mAEsml3thLmu50Dw"
    }

    urls = ["http://localhost:8080", "http://localhost:8000"]

    result = otp.postOtpBlob(data, sk, urls)

    print(result)

Output
^^^^^^

.. code:: json

    {
        "http://localhost:8000": {
            "data": {
                "otp_data": {
                    "id": "did:dad:V7A6qo1D8VG7ZXF2h1vVeANPHrcmljPgpBNb2c4g2wA=", 
                    "blob": "AeYbsHot0pmdWAcgTo5sD8iAuSQAfnH5U6wiIGpVNJQQoYKBYrPPxAoIc1i5SHCIDS8KFFgf8i0tDq8XGizaCgo9yjuKHHNJZFi0QD9K6Vpt6fP0XgXlj8z_4D-7s3CcYmuoWAh6NVtYaf_GWw_2sCrHBAA2mAEsml3thLmu50Dw", 
                    "changed": "2018-07-16T21:16:50.056107+00:00"
                }, 
                "signatures": {
                    "signer": "b1M0f78dfMWYBpDaM7sQujmGh1HWlcLjTW7BTrIyCoXBXsrOltEXa_K--Sblox1BCoBpSZ8k0uvN0j88P12DAQ=="
                }
            }, 
            "http_status": 201
        }, 
        "http://localhost:8080": {
            "data": {
                "otp_data": {
                    "id": "did:dad:V7A6qo1D8VG7ZXF2h1vVeANPHrcmljPgpBNb2c4g2wA=", 
                    "blob": "AeYbsHot0pmdWAcgTo5sD8iAuSQAfnH5U6wiIGpVNJQQoYKBYrPPxAoIc1i5SHCIDS8KFFgf8i0tDq8XGizaCgo9yjuKHHNJZFi0QD9K6Vpt6fP0XgXlj8z_4D-7s3CcYmuoWAh6NVtYaf_GWw_2sCrHBAA2mAEsml3thLmu50Dw", 
                    "changed": "2018-07-16T21:16:50.056107+00:00"
                }, 
                "signatures": {
                    "signer": "b1M0f78dfMWYBpDaM7sQujmGh1HWlcLjTW7BTrIyCoXBXsrOltEXa_K--Sblox1BCoBpSZ8k0uvN0j88P12DAQ=="
                }
            }, 
            "http_status": 201
        }
    }

otping.putOtpBlob(data, sk, urls)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

putOtpBlob sends an updated otp encrypted blob to the didery servers.
putOtpBlob returns a dictionary of url, response key pairs

| **data** (*required*)- otp encrypted blob data as specified in the
  `didery
  documentation <https://github.com/reputage/didery/wiki/Public-API#add-otp-encrypted-key>`__
| **sk** (*required*)- current signing key. base64 url-file safe
  signing/private key from EdDSA (Ed25519) key pair
| **urls** (*required*)- list of url strings to query

Example
^^^^^^^

.. code:: python

    import diderypy.lib.otping as otp
    import diderypy.lib.generating as gen

    # make sure there is already data on the server for our did 
    vk, sk, did = gen.keyGen()

    data = {
        "id": did,
        "blob": "AeYbsHot0pmdWAcgTo5sD8iAuSQAfnH5U6wiIGpVNJQQoYKBYrPPxAoIc1i5SHCIDS8KFFgf8i0tDq8XGizaCgo9yjuKHHNJZFi0QD9K6Vpt6fP0XgXlj8z_4D-7s3CcYmuoWAh6NVtYaf_GWw_2sCrHBAA2mAEsml3thLmu50Dw"
    }

    urls = ["http://localhost:8080", "http://localhost:8000"]

    otp.postOtpBlob(data, sk, urls)

    # Update data on the server 
    data["blob"] = "OtjioHot0pmdWAcgTo5sD8iAuSQAfnH5U6wiIGpVNJQQoYKBYrPPxAoIc1i5SHCIDS8KFFgf8i0tDq8XGizaCgo9yjuKHHNJZFi0QD9K6Vpt6fP0XgXlj8z_4D-7s3CcYmuoWAh6NVtYaf_GWw_2sCrHBAA2mAEsml3thLmu50Dw"

    result = otp.putOtpBlob(data, sk, urls)

    print(result)

Output
^^^^^^

.. code:: json

    {
        "http://localhost:8000": {
            "data": {
                "otp_data": {
                    "id": "did:dad:Hz3XqAcXUPhiGH_OH65DfBVikYyT8A27Oe6X203Ktp8=", 
                    "blob": "OtjioHot0pmdWAcgTo5sD8iAuSQAfnH5U6wiIGpVNJQQoYKBYrPPxAoIc1i5SHCIDS8KFFgf8i0tDq8XGizaCgo9yjuKHHNJZFi0QD9K6Vpt6fP0XgXlj8z_4D-7s3CcYmuoWAh6NVtYaf_GWw_2sCrHBAA2mAEsml3thLmu50Dw", 
                    "changed": "2018-07-16T21:27:53.028815+00:00"
                }, 
                "signatures": {
                    "signer": "-UgO0QssuQbhOKPJxB4JCqfWho1lwUh018C0Rxkk2ZI_PDJKqPNfS9DwUNV1JbYeZMpO-RC-zhOdgWKxjr1dBg=="
                }
            }, 
            "http_status": 200
        }, 
        "http://localhost:8080": {
            "data": {
                "otp_data": {
                    "id": "did:dad:Hz3XqAcXUPhiGH_OH65DfBVikYyT8A27Oe6X203Ktp8=", 
                    "blob": "OtjioHot0pmdWAcgTo5sD8iAuSQAfnH5U6wiIGpVNJQQoYKBYrPPxAoIc1i5SHCIDS8KFFgf8i0tDq8XGizaCgo9yjuKHHNJZFi0QD9K6Vpt6fP0XgXlj8z_4D-7s3CcYmuoWAh6NVtYaf_GWw_2sCrHBAA2mAEsml3thLmu50Dw", 
                    "changed": "2018-07-16T21:27:53.028815+00:00"
                }, 
                "signatures": {
                    "signer": "-UgO0QssuQbhOKPJxB4JCqfWho1lwUh018C0Rxkk2ZI_PDJKqPNfS9DwUNV1JbYeZMpO-RC-zhOdgWKxjr1dBg=="
                }
            }, 
            "http_status": 200
        }
    }

otping.getOtpBlob(did, urls)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

getOtpBlob accepts a W3C decentralized
identifier(\ `DID <https://w3c-ccg.github.io/did-spec/>`__) string and a
list of urls to poll. getOtpBlob returns a single otp blob if 2/3 of the
urls returned matching data. If less than 2/3 returned matching data
None is returned.

| **did** (*required*)- W3C decentralized
  identifier(\ `DID <https://w3c-ccg.github.io/did-spec/>`__) string
| **urls** (*required*)- list of url strings to query

**returns** - (dict, dict) containing the otp encrypted blob as shown on
the didery documentation and a results dict containing a short string
description for each url. The results dict can be used to determine what
urls failed and why.

Example
^^^^^^^

.. code:: python

    import diderypy.lib.otping as otp
    import diderypy.lib.generating as gen

    # generate a did for the data
    vk, sk, did = gen.keyGen()

    data = {
        "id": did,
        "blob": "AeYbsHot0pmdWAcgTo5sD8iAuSQAfnH5U6wiIGpVNJQQoYKBYrPPxAoIc1i5SHCIDS8KFFgf8i0tDq8XGizaCgo9yjuKHHNJZFi0QD9K6Vpt6fP0XgXlj8z_4D-7s3CcYmuoWAh6NVtYaf_GWw_2sCrHBAA2mAEsml3thLmu50Dw"
    }

    urls = ["http://localhost:8080", "http://localhost:8000"]

    # data must already exist for getOtpBlob to work
    otp.postOtpBlob(data, sk, urls)

    # retrieve the otp data
    data, results = otp.getOtpBlob(did, urls)

    if data is None:
        # Consensus could not be reached. Print results for each url
        for url, result in results.items():
            print("{}:\t{}".format(url, result))
    else:
        print(data)

Output
^^^^^^

.. code:: json

    {
        "otp_data": {
            "id": "did:dad:xe5I8KgW7OkeZ6x5oHtfx5NQyJWOnoFZ_djOZr0dGz0=", 
            "blob": "AeYbsHot0pmdWAcgTo5sD8iAuSQAfnH5U6wiIGpVNJQQoYKBYrPPxAoIc1i5SHCIDS8KFFgf8i0tDq8XGizaCgo9yjuKHHNJZFi0QD9K6Vpt6fP0XgXlj8z_4D-7s3CcYmuoWAh6NVtYaf_GWw_2sCrHBAA2mAEsml3thLmu50Dw", "changed": "2018-07-16T21:38:04.899640+00:00"
        }, 
        "signatures": {
            "signer": "Az-qzuaOu1xelHU9quxPMZynZZAdc1BzqUchmJVIPUsFB7QdLBnHB_CXNdGK6okkDaCaxXCsyk4icQBW_dqLDA=="
        }
    }

historying.removeOtpBlob(did, sk, urls)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For GDPR compliance a delete method is provided. For security reasons
the data cannot be deleted without signing with the signing key
associated with the public key in the did.

| **did** (*required*)- W3C decentralized
  identifier(\ `DID <https://w3c-ccg.github.io/did-spec/>`__) string
  **sk** (*required*)- current signing key. base64 url-file safe
  signing/private key from EdDSA (Ed25519) key pair
| **urls** (*required*)- list of url strings to query

**returns** - dict containing the one time pad encrypted keys that were
deleted.

Example
^^^^^^^

.. code:: python

    import diderypy.lib.otping as otp
    import diderypy.lib.generating as gen

    # generate a did for the data
    vk, sk, did = gen.keyGen()

    data = {
        "id": did,
        "blob": "AeYbsHot0pmdWAcgTo5sD8iAuSQAfnH5U6wiIGpVNJQQoYKBYrPPxAoIc1i5SHCIDS8KFFgf8i0tDq8XGizaCgo9yjuKHHNJZFi0QD9K6Vpt6fP0XgXlj8z_4D-7s3CcYmuoWAh6NVtYaf_GWw_2sCrHBAA2mAEsml3thLmu50Dw"
    }

    urls = ["http://localhost:8080", "http://localhost:8000"]

    # data must already exist for getOtpBlob to work
    otp.postOtpBlob(data, sk, urls)

    # delete the otp encrypted data
    response = otp.removeOtpBlob(did, sk, urls)

    print(response)

Output
^^^^^^

.. code:: json

    {
        "http://localhost:8000": {
            "data": {
                "deleted": {
                    "otp_data": {
                        "id": "did:dad:pq4ovXgMGYILIfW9Vx55-ebugLWA-7Ii6qLnPUjZVFk=", 
                        "blob": "AeYbsHot0pmdWAcgTo5sD8iAuSQAfnH5U6wiIGpVNJQQoYKBYrPPxAoIc1i5SHCIDS8KFFgf8i0tDq8XGizaCgo9yjuKHHNJZFi0QD9K6Vpt6fP0XgXlj8z_4D-7s3CcYmuoWAh6NVtYaf_GWw_2sCrHBAA2mAEsml3thLmu50Dw", 
                        "changed": "2018-08-02T21:45:30.795185+00:00"
                    }, 
                    "signatures": {
                        "signer": "9ZIRyzBh9WkVaksQoUlBRB_Zrlg8kjcepjcOvPTSjj784uYVGusWiDkSq3nOyTp78v_eHEbzDEKFw6WscN6uAw=="
                    }
                }
            }, 
            "http_status": 200
        }, 
        "http://localhost:8080": {
            "data": {
                "deleted": {
                    "otp_data": {
                        "id": "did:dad:pq4ovXgMGYILIfW9Vx55-ebugLWA-7Ii6qLnPUjZVFk=", 
                        "blob": "AeYbsHot0pmdWAcgTo5sD8iAuSQAfnH5U6wiIGpVNJQQoYKBYrPPxAoIc1i5SHCIDS8KFFgf8i0tDq8XGizaCgo9yjuKHHNJZFi0QD9K6Vpt6fP0XgXlj8z_4D-7s3CcYmuoWAh6NVtYaf_GWw_2sCrHBAA2mAEsml3thLmu50Dw", 
                        "changed": "2018-08-02T21:45:30.795185+00:00"
                    }, 
                    "signatures": {
                        "signer": "9ZIRyzBh9WkVaksQoUlBRB_Zrlg8kjcepjcOvPTSjj784uYVGusWiDkSq3nOyTp78v_eHEbzDEKFw6WscN6uAw=="
                    }
                }
            }, 
            "http_status": 200
        }
    }
