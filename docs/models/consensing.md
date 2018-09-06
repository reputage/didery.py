# models.consensing.py

## ConsensusResult

ConsensusResult object is a container class for storing info about a request and the status of a requests validation during the consensing step. A list or dict of ConsensusResult objects will be returned by any function running didery.py's consensing algorithm.

_class_ models.consensing.**ConsensusResult**(url, validation_status, response=None, http_status=None)

**url** (_required_): url string that was queried     
**validation_status** (_required_): integer value between 0 and 3  
**response** (_optional_): dict or model containing response data from the above url  
**http_status** (_optional_): integer representing the http response status from the request

#### Static Attributes

The ConsensusResult object has a few static attributes to identify the result of the signature validation 

**TIMEOUT** - The request timed out  
**VALID** - The signatures were verified to be valid  
**ERROR** - There was an error while making the request  
**FAILED** - The signatures failed validation  

#### Example Usage
```python
from pydidery.models.consensing import ConsensusResult

# setup the result object
result = ConsensusResult("http://localhost:8080", ConsensusResult.VALID)

if result.validation_status == ConsensusResult.FAILED:
    print("Invalid Signature")
elif result.validation_status == ConsensusResult.TIMEOUT:
    print("Server could not be reached")
elif result.validation_status == ConsensusResult.ERROR:
    print("Error while contacting the server")
elif result.validation_status == ConsensusResult.VALID:
    print("Signatures are valid")

# Alternatively ConsensusResult overloads the __str__ and can give the same result as above
print()
print(str(result))
```

#### Output
```
Signatures are valid

http://localhost:8080:	Signature Validation Succeeded
```

#### Attributes
**url** - url string that was queried     

**validation_status** - integer value between 0 and 3  

**response** - dict or model containing response data from the above url  

**http_status** - integer representing the http response status from the request
