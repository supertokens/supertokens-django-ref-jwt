---
id: manipulating-session-info
title: Manipulating Session Info
sidebar_label: Manipulating Session Info
---

## There are two types of data you can store in a session:
- ```jwt_payload```
    - Once set, it cannot be changed further.
    - Should not contain any sensitive information since this is sent over to the client.
    - Once you have a ```Session``` object, fetching the ```jwt_payload``` does not require any database calls.
- ```session_info```
    - This can be changed anytime during the lifetime of a session.
    - Can contain sensitive information since this is only stored in your database.
    - Requires a database call to read or write this information.
    - Fetching or modification of this is not synchronized per session.

## If you have a session object
Please see the [Session Object](session-object#call-the-get_session_info-function-api-reference-api-reference-sessionget_session_info) section for more information.

## If you do not have a session object
<div class="specialNote">
These functions should only be used if absolutely necessary, since they do not handle cookies for you. So if you are able to get a <code>Session</code> object AND have not already sent a reply to the client, please use the functions from the above section instead.
</div>

### Call the ```get_session_info``` function: [API Reference](api-reference#get_session_infosession_handle)
```python
SuperTokens.get_session_info(session_handle);
```
- This function requires a database call each time it's called.

### Call the ```update_session_data``` function: [API Reference](api-reference#update_session_infosession_handle-info)
```python
SuperTokens.update_session_data(session_handle, new_session_info);
```
- This function overrides the current data stored for this ```session_handle```.
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

# method 1: using session object
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
session = None
try:
    session = supertokens.get_session(request, response, enable_csrf_protection)
except:
    ...
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

# method 2: using session handle
def update_session_info(session_info):
    try:
        session_info = supertokens.get_session_info(session_handle)
        new_session_info = {**session_info, 'joke': 'Knock, knock'}
        supertokens.update_session_info(session_handle, new_session_info)
    except SuperTokensGeneralException:
        response.status_code = 500
        response.data = "Something went wrong"
        return response
    except SuperTokensUnauthorizedException:
        response.status_code = 440
        response.data = "Session expired! Please login again"
        return response
```