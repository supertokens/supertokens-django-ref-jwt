---
id: exception-handling
title: Exception Handling
sidebar_label: Exception Handling
---

## All our functions will throw one of these four types of exceptions:

- ```SuperTokensGeneralException```
- ```SuperTokensUnauthorizedException```
- ```SuperTokensTokenTheftException```
- ```SuperTokensTryRefreshTokenException```

### ```SuperTokensGeneralException```
- This is the most general type of exception. Can be raised for a variety of reasons:
    - Database issues - not reachable, instance crash, etc.
    - Generic "Something went wrong" errors.
- The way to handle this exception is to simply send a status code of ```500```.

### ```SuperTokensUnauthorizedException```
- This exception is raised when the library is sure that this user's session does not exist anymore. This can happen:
    - If the refresh token expires.
    - If the user clears the cookies.
    - If the session has been revoked or the user has logged out
- The way to handle this exception is to ask the user to login again.

### ```SuperTokensTokenTheftException```
- This is raised when we detect token theft.
- Handling this exception, you can revoke the affected user's current session, or all their sessions.
- The way to handle this exception is to ask the user to login again.

### ```SuperTokensTryRefreshTokenException```
- This exception is raised when:
    - Access token validation failed.
    - CSRF token validation failed. (If in ```settings.py```, ```ANTI_CSRF_ENABLE``` in the ```SUPER_TOKENS``` object is set to ```True``` (default: True))
- The way to handle this exception is to <span class="highlighted-text"><b>NOT</b> clear the cookies</span> and send a session expired status code to your frontend. Our frontend SDK will take care of calling your refresh token API for you.
- If you are building a website and get this error for a <code>GET API</code> that returns <code>HTML</code>, then you should reply with  <code>HTML & JS</code> that calls your refresh session endpoint. Once that is successful, your frontend code should redirect the browser to call again the original <code>GET</code> API. More details on this in the frontend section.