---
id: options-api
title: Handling Options API
sidebar_label: Handling Options API
---

<div class="specialNote">
This section is only applicable to web browser based apps.
</div>
<div style="height: 20px"></div>

The primary purpose of an ```Options``` API is to enable CORS.

## Call the ```set_headers_for_options_api``` function: [API Reference](api-reference#set_headers_for_options_apiresponse)
```python
supertokens.set_headers_for_options_api(response);
```
- Adds the following headers to the response:
    - ```Access-Control-Allow-Headers```: ```"anti-csrf"```
    - ```Access-Control-Allow-Credentials```: ```true```

<div class="divider"></div>

## Example code
```python
from rest_framework.response import Response
# you can also use HttpResponse from django.http or any
# response method which is extended from HttpResponse
from supertokens_jwt_ref import supertokens

# inside your view function for options API
...
response = Response()
...
supertokens.set_headers_for_options_api(response)
...
return response
```