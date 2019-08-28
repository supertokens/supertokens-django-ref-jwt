---
id: user-logout
title: User Logout
sidebar_label: User Logout
---

- Logging out a user from a particular device can be done via revoking that user session - either via a ```Session``` object, or via a ```session_handle```. 

- If you want to revoke all sessions belonging to a user, you will only need their ```user_id```.

<div class="specialNote">
If you can get the <code>Session</code> object, use that since revoking a session using that will also take care of clearing the cookies for you. 
</div>

## If you have a ```Session``` object
Please see the [Session Object](session-object#call-the-revoke_session-function-api-reference-api-reference-sessionrevoke_session) section for more information.

## If you have a ```session_handle```
### Call the ```revoke_session``` function: [API Reference](api-reference#revoke_sessionsession_handle)
```python
supertokens.revoke_session(session_handle);
```
- Use this to logout a user from their current session
- <span class="highlighted-text">Does not clear any cookies</span>

## If you have a ```user_id```
### Call the ```revoke_all_sessions_for_user``` function: [API Reference](api-reference#revoke_all_sessions_for_useruser_id)
```python
supertokens.revoke_all_sessions_for_user(user_id);
```
- Use this to logout a user from all their devices.
- <span class="highlighted-text">Does not clear any cookies</span>

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

# method 1: example using Session object
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
    # See verify session page to handle errors here.
    ...
...
# revoking session example
try:
    session.revoke_session()
    # session has been destroyed
except SuperTokensGeneralException:
    response.status_code = 500
    response.data = "Something went wrong"
    return response
...

# --------------------------------------------
# method 2: example using session_handle
def logout_using_session_handle(session_handle):
    try:
        success = supertokens.revoke_session(session_handle)
        if success:
            # your code here..
        else:
            # either sessionHandle is invalid, or session was already removed.
            # your code here..
    except SuperTokensGeneralException:
        response.status_code = 500
        response.data = "Something went wrong"
        return response
    ...

# --------------------------------------------
# method 3: example using user_id
def logout_all_sessionsFor_user(user_id):
    try:
        supertokens.revoke_all_sessions_for_user(session_handle)
    except SuperTokensGeneralException:
        response.status_code = 500
        response.data = "Something went wrong"
        return response
    ...
```