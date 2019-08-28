---
id: user-login
title: User login
sidebar_label: User login
---
To login a user, you must first authenticate their credentials and then create a session for them so that they can access your APIs.

## Call the ```create_new_session``` function: [API Reference](api-reference#create_new_sessionresponse-user_id-jwt_payload-none-session_info-none)
```python
supertokens.create_new_session(response, user_id, jwt_payload, session_info)
```
- Call this function after you have verified the user credentials.
- This will override any existing session that exists in the ```response``` object with a new session.
- ```jwt_payload``` should not contain any sensitive information.

<div class="divider"></div>

## Example code
```python
from rest_framework.response import Response
# you can also use HttpResponse from django.http or any
# response method which is extended from HttpResponse
from supertokens_jwt_ref import supertokens

# inside your view function
...
user_id = "User1" # authentication will be done by you
jwt_payload = { 'userId': 'user_id', 'name': 'spooky action at a distance'};
session_info = {'awesomeThings': ['programming', 'python', 'supertokens']};
response = Response()
...
supertokens.create_new_session(response, user_id, jwt_payload, session_info)
...
return response
```