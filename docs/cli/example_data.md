# Example Data File
A data file can contain a history json object, a otp json object, or both.  You can specify the path to the file using the --data cli option.

#### data.json
```json
{
    "history": {
        "id": "did:dad:LYyYqfpFLbRcqqah3ViCBPl-c0wW5qo7IpT9Fl13I4Q=",
        "signer": 1,
        "signers":
        [
            "LYyYqfpFLbRcqqah3ViCBPl-c0wW5qo7IpT9Fl13I4Q=",
            "CQPaPAhXN0zS0pP94ms1usKlCPUK1GBXBlCSlXMX02U=",
            "qofdqNFvYbi52ZzaVM9hB0i8hUNbUQRZkhpHFpyYcfU="
        ]
    },
    "otp": {
        "blob": "AeYbsHot0pmdWAcgTo5sD8iAuSQAfnH5U6wiIGpVNJQQoYKBYrPPxAoIc1i5SHCIDS8KFFgf8i0tDq8XGizaCgo9yjuKHHNJZFi0QD9K6Vpt6fP0XgXlj8z_4D-7s3CcYmuoWAh6NVtYaf_GWw_2sCrHBAA2mAEsml3thLmu50Dw",
        "id": "did:dad:LYyYqfpFLbRcqqah3ViCBPl-c0wW5qo7IpT9Fl13I4Q="
    }
}
```