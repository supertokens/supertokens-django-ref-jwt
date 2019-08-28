---
id: version-1.0.X-refreshing-session
title: Refreshing Session
sidebar_label: Refreshing Session
original_id: refreshing-session
---

This operation is to be done whenever any function returns the ```SuperTokensTryRefreshTokenException``` exception.

### The following are the steps that describe how this works:
- Your frontend calls an API (let's say ```/getHomeFeed```) with an access token that has expired.
- In that API, your backend calls the ```supertokens.getSession(request, response, enable_csrf_protection)``` function which throws a ```SuperTokensTryRefreshTokenException``` exception.
- Your backend replies with a session expired status code to your frontend.
- Your frontend detects this status code and calls an API on your backend that will refresh the session (let's call this API ```/api/refresh```).
- In this API, you call the ```supertokens.refresh_session(request, response)``` function that "refreshes" the session. This will result in the generation of a new access and a new refresh token. The lifetime of these new tokens starts from the point when they were generated (Please contact us if this is unclear).
- Your frontend then calls the ```/getHomeFeed``` API once again with the new access token yielding a successful response.

Our frontend SDK takes care of calling your refresh session endpoint and managing the auth tokens on your frontend.

<div class="specialNote">
If you are building a webapp and get a <code>SuperTokensTryRefreshTokenException</code> excpetion on your backend for a <code>GET</code> request that returns <code>HTML</code>, then you should reply with  <code>HTML & JS</code> code that calls your <code>/api/refresh</code> endpoint. Once that is successful, your frontend code should redirect the browser to call again the original <code>GET</code> API. More details on this in the frontend section.
</div>

## Call the ```refresh_session``` function: [API Reference](api-reference#refresh_sessionrequest-response)
```python
supertokens.refresh_session(request, response);
```
- Refreshes the session by generating new access and new refresh tokens.
- If token theft is detected, then it throws a special ```SuperTokensTokenTheftException``` exception. Using this exception object, you can see who the affected user is and can choose to revoke their affected session.
- <span class="highlighted-text">This function should only be called in a special ```POST``` API endpoint whose only job is to refresh the session.</span> The path to this API will have to be given in the [Configurations](initialisation#configurations) ```(renewTokenPath)``` so that the refresh token cookie path can be set correctly.

<div class="divider"></div>

## Example code
```python
from rest_framework.response import Response
# you can also use HttpResponse from django.http or any
# response method which is extended from HttpResponse
from supertokens_jwt_ref import supertokens
from supertokens_jwt_ref.exceptions import (
    SuperTokensUnauthorizedException,
    SuperTokensTokenTheftException,
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
try:
    supertokens.refresh_session(request, response)
except SuperTokensGeneralException:
    response.status_code = 500
    response.data = "Something went wrong"
    return response
except SuperTokensUnauthorizedException:
    response.status_code = 440
    response.data = "Session expired! Please login again"
    return response
except SuperTokensTokenTheftException as e:
    # we have detected token theft! 
    # get the affected user details
    user_id = e.get_user_id()
    session_handle = e.get_session_handle()
    # we can now revoke this session or all sessions belonging to this user.
    # we can also alert this user if needed.
    response.status_code = 440
    response.data = "Session expired! Please login again"
    return response

# on success
response.status_code = 200
response.data = "Successful refreshing of session!"
return response
```