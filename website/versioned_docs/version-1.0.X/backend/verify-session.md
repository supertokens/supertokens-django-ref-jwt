---
id: version-1.0.X-verify-session
title: Verify Session
sidebar_label: Verify Session
original_id: verify-session
---

## Call the ```get_session``` function: [API Reference](api-reference#get_sessionrequest-response-enable_csrf_protection)
```python
supertokens.get_session(request, response, enable_csrf_protection);
```
- Use this function at the start of each API call to authenticate the user. 
- Call the function directly in each API.
- This will return a ```Session``` object. Please see the next section for information with what you can do with this.

<div class="divider"></div>

## Example code
```python
from rest_framework.response import Response
# you can also use HttpResponse from django.http or any
# response method which is extended from HttpResponse
from supertokens_jwt_ref import supertokens
from supertokens_jwt_ref.exceptions import (
    SuperTokensUnauthorizedException,
    SuperTokensTryRefreshTokenException,
    SuperTokensGeneralException
)

# inside your view function
...
response = Response()
...
# request parameter will be available in your view function
# e.g.
#   def get_some_details(request):
#       ...
#
# OR if you are using something like APIView:
#   class UserList(APIView):
#       def get(self, request):
#           ...
enable_csrf_protection = True # if you want to enable custom CSRF protection by supertokens (recommended)
try:
    session = supertokens.get_session(request, response, enable_csrf_protection)
except SuperTokensGeneralException:
    response.status_code = 500
    response.data = "Something went wrong"
    return response
except SuperTokensUnauthorizedException:
    response.status_code = 440
    response.data = "Session expired! Please login again"
    return response
except SuperTokensTryRefreshTokenException:
    response.status_code = 440
    response.data = "Please call refresh token endpoint"
    return response
...
```
