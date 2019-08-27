---
id: session-handle
title: Session Handle
sidebar_label: Session Handle
---

A ```session_handle``` is a unique ID for a session in your system. It stays the same during the entire lifetime a session - even though the actual access and refresh tokens keep changing.

## How do you get a ```session_handle```?
- You can call the ```get_all_session_handles_for_user``` function (see below)
- If token theft is detected, then you can call the ```get_session_handle``` method on the ```exception``` object to get the ```session_handle```.

## What can you do with a ```session_handle```?
- Revoke a session: See "User Logout" section.
- Update session information: See "Manipulating Session Data" section.

## Call the ```get_all_session_handles_for_user``` function: [API Reference](api-reference#getallsessionhandlesforuseruserid)
```python
SuperTokens.get_all_session_handles_for_user(user_id)
```
- This function requires a database call.

<div class="divider"></div>

## Example code
```python
from supertokens_jwt_ref import supertokens

def session_handle_func(user_id):
    ...
    session_handles = supertokens.get_all_session_handles_for_user(user_id)
    for session_handle in session_handles:
        # do something with the current session
    ...
```