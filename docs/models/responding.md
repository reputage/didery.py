# responding.py

## DideryResponse

DideryResponse object is a container class for storing info about a HTTP response.

_class_ models.responding.**DideryResponse**(url, status, response)

**url** (_required_): url string that was queried     
**status** (_required_): integer representing the http response status from the request  
**response** (_optional_): dict or model containing response data from the above url  

#### Attributes
**url** - url string that was queried     

**status** - integer representing the http response status from the request

**response** - dict or model containing response data from the above url

## AbstractDideryData

AbstractDideryData object is an abstract parent class for storing response data from didery servers.

#### Attributes

**data** - dict containing response data from didery servers   

**bdata** - byte string version of response data   

**body** - parsed data from data dict   

**bbody** - byte string version of body data   

**vk** - current verifier/public key stored in a url-file safe base64 string   

**did** - W3C DID string   

**signature** - url-file safe base64 signature string   

**valid** - When this attribute is accessed the signature is verified against the bbody data and a bool is returned.

##  HistoryData

HistoryData is a container class that implements the AbstractDideryData class.  It adds three additional attributes to the base class.

_class_ models.responding.**HistoryData**(data)

**data** (_required_): dict returned from request to /history/ endpoint on didery servers 

#### Attributes

**previous_vk** - previous verifier/public key stored in a url-file safe base64 string   

**signer_sig** - url-file safe base64 signer signature string   

**rotation_sig** - if a rotation signature was sent with the response data it will contain a url-file safe base64 rotation signature string otherwise None is returned.

**valid** - the valid attribute will verify both the signer and the rotation signature if it was included with the data.  If only one signature is valid the attribute will be false.

## OtpData

OtpData is a container class that implements the AbstractDideryData class.  It does not currently add any additional attributes or methods to the base class.

_class_ models.responding.**HistoryData**(data)

**data** (_required_): dict returned from request to /blob/ endpoint on didery servers

## responseFactory

responseFactory()  implements the factory pattern to build objects for history, otp, and events data based on the format of the data that is passed to it. 

##### models.responding.responseFactory(url, status, data)
**url** (_required_): url string that was queried     
**status** (_required_): integer representing the http response status from the request  
**response** (_optional_): dict containing response data from the above url

**returns** - DideryResponse object containing in it's response field either a HistoryData object, OtpData object, or a dict of HistoryData objects depending on if you passed rotation history data, otp encrypted blob data, or events data.  