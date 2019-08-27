---
id: session-object
title: Session Object
sidebar_label: Session Object
---

A ```Session``` object is returned when a session is verified successfully. Following are the functions you can use on this ```session``` object:
```python
session = supertokens.get_session(request, response, enable_csrf_protection)
```
<div class="specialNote">
Please only use this session object if you have not sent a reply to the client yet.
</div>

## Call the ```get_user_id``` function: [API Reference](../api-reference#sessiongetuserid)
```python
session.get_user_id()
```
- This function does not do any database call.

## Call the ```get_jwt_payload``` function: [API Reference](../api-reference#sessiongetjwtpayload)
```python
session.get_jwt_payload()
```
- This function does not do any database call.
- It reads the payload available in the JWT access token that was used to verify this session.

## Call the ```revoke_session``` function: [API Reference](../api-reference#sessionrevokesession)
```python
session.revoke_session()
```
- Use this to logout a user from their current session.
- This function deletes the session from the database and clears relevant auth cookies
- If using ```blacklisting```, this will immediately invalidate the ```JWT``` access token. If not, the user may still be able to continue using their access token to call authenticated APIs (until it expires).

## Call the ```get_session_info``` function: [API Reference](../api-reference#sessiongetsessiondata)
```js
session.get_session_info()
```
- This function requires a database call each time it's called.

## Call the ```update_session_info``` function: [API Reference](../api-reference#sessionupdatesessiondatadata)
```js
session.update_session_info(info)
```
- This function overrides the current session info stored for this session.
- This function requires a database call each time it's called.

<div class="divider"></div>

## Example code
```python
from rest_framework.response import Response
# you can also use HttpResponse from django.http or any
# response method which is extended from HttpResponse
from supertokens_jwt_ref import supertokens
from supertokens_jwt_ref.exceptions import (
    SuperTokensUnauthorizedException,
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

# first we get the session object.
session = supertokens.get_session(request, response, enable_csrf_protection)
user_id = session.get_user_id()
jwt_payload = session.get_jwt_payload()

...

# update session info example
try:
    session_info = session.get_session_info()
    new_session_info = {**session_info, 'joke': 'Knock, knock'}
    session.update_session_info(new_session_info)
except SuperTokensGeneralException:
    response.status_code = 500
    response.data = "Something went wrong"
    return response
except SuperTokensUnauthorizedException:
    response.status_code = 440
    response.data = "Session expired! Please login again"
    return response

...

# revoking session example
try:
    session.revoke_session()
    # session has been destroyed
except SuperTokensGeneralException:
    response.status_code = 500
    response.data = "Something went wrong"
    return response
```
