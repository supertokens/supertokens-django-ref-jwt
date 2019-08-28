---
id: api-reference
title: API Reference
sidebar_label: API Reference
---

## ```create_new_session(response, user_id, jwt_payload=None, session_info=None)```
##### Parameters
- ```response```
    - Type: ```Response``` from ```rest_framework.response``` or you can also use ```HttpResponse``` from ```django.http``` or any response method which is extended from HttpResponse
- ```user_id```
    - Type: ```string | number```
    - Should be used to ID a user in your system.
- ```jwt_payload``` (Optional)
    - Type: ```object | array | number | string | boolean | None``` 
    - This information is stored in the JWT sent to the frontend, so <span class="highlighted-text">it should not contain any sensitive information.</span>
    - Once set, it cannot be changed during the lifetime of a session.
- ```session_info``` (Optional)
    - Type: ```object | array | number | string | boolean | None``` 
    - This information is stored only in your database, so <span class="highlighted-text">it can contain sensitive information if needed.</span>
    - This can be freely modified during the lifetime of a session. But we do not synchronize calls to modify this - you must take care of locks yourself.
##### Returns
- ```Session``` on successful creation of a session
##### Throws
- ```SuperTokensGeneralException```
    - Examples of when this is thorwn is if the library could not connect to the database.
##### Additional information
- Creates a new access and a new refresh token for this session.
- This function will set the following cookies and headers in the ```response``` object for you:
    - If in ```settings.py```, ```ANTI_CSRF_ENABLE``` in the ```SUPER_TOKENS``` object is set to ```True``` (default: True), it sets ```anti-csrf``` header that contains an anti-csrf token. This header should be sent for all non-GET API calls that require authentication (except for the refresh session API). 
    - Sets ```sAccessToken``` in cookies with the access token. This cookie has ```HttpOnly``` set to ```True``` and ```secure``` set to ```True``` depending on your passed config. This cookie should be sent for all API calls that require authentication. 
    - Sets ```sRefreshToken``` in cookies containing the refresh token. This cookie has ```HttpOnly``` set to ```True``` and ```secure``` set to ```True``` depending on your passed config. <span class="highlighted-text">This cookie should be sent only to the refresh token API.</span>
    - Sets ```sIdRefreshToken``` in cookies containing a unique ID. Details for why this is needed can be found in the "How it works" section. This cookie has ```HttpOnly``` set to ```False``` and ```secure``` set to ```False```. This cookie should be sent for all API calls that require authentication. 
- Inserts a new row in the MySQL table for this new session.

<div class="divider"></div>

## ```get_session(request, response, enable_csrf_protection)```
##### Parameters
- ```request```
    - Type: request parameter that is available in your view function (e.g. ```django.http.HttpRequest```)
- ```response```
    - Type: ```Response``` from ```rest_framework.response``` or you can also use ```HttpResponse``` from ```django.http``` or any response method which is extended from HttpResponse
- ```enableCsrfProtection```
    - Type: ```boolean```
    - If in ```settings.py```, ```ANTI_CSRF_ENABLE``` in the ```SUPER_TOKENS``` object is set to ```False```, this value will be considered as ```False``` even if value ```True``` is passed
##### Returns
- ```Session``` on successful verification of a session
##### Throws
- ```SuperTokensGeneralException```
    - Examples of when this is thorwn is if the library could not connect to the database.
- ```SuperTokensUnauthorizedException```
    - This is thorwn if the ```idRefreshToken``` cookie is missing from the ```request``` object or if the session has been revoked.
    - When this is thorwn, all the relevant auth cookies are cleared by this function call, so you can redirect the user to a login page.
- ```SuperTokensTryRefreshTokenException```
    - This will be thorwn if JWT verification fails. This happens, for example, if the token has expired or the JWT signing key has changed.
    - This will be thorwn if ```enable_csrf_protection``` is ```True```, `in ```settings.py```, ```ANTI_CSRF_ENABLE``` in the ```SUPER_TOKENS``` object is set to ```True``` (default: True) and ```anti-csrf``` token validation fails.
    - When this is thorwn, none of the auth cookies are removed - you should return a ```session expired``` status code and instruct your frontend to call the refresh token API endpoint. Our frontend SDK takes care of this for you in most cases.
##### Additional information
- Verifies the current session using the ```request``` object.
- This function will mostly never require a database call since we are using JWT access tokens unless ```blacklisting``` is enabled.
- If ```enable_csrf_protection``` is ```True```, `in ```settings.py```, ```ANTI_CSRF_ENABLE``` in the ```SUPER_TOKENS``` object is set to ```True``` (default: True), this function also provides CSRF protection. We strongly recommend that you set it to true for any non-GET API that requires user auth (except for the refresh session API).
- May change the access token - but this is taken care of by this function and our frontend SDK. You do need to worry about handling this.

<div class="divider"></div>

## ```session.get_user_id()```
##### Parameters
- none
##### Returns
- ```string | number``` - unique ID passed to the library when creating this session.
##### Throws
- nothing

<div class="divider"></div>

## ```session.get_jwt_payload()```
##### Parameters
- none
##### Returns
- ```object | array | number | string | boolean | None``` - Will be deeply equal to whatever was passed to the ```create_new_session``` function.
##### Throws
- nothing

<div class="divider"></div>

## ```session.revoke_session()```
##### Parameters
- none
##### Returns
- nothing
##### Throws
- ```SuperTokensGeneralException```
    - Examples of when this is thorwn is if the library could not connect to the database.

<div class="divider"></div>

## ```session.get_session_info()```
##### Parameters
- none
##### Returns
- ```object | array | number | string | boolean | None>``` - The result will be deeply equal to whatever was passed to the ```create_new_session``` function.
##### Throws
- ```SuperTokensGeneralException```
    - Examples of when this is thorwn is if the library could not connect to the database.
- ```SuperTokensUnauthorizedException```
    - This is thorwn if the current session was revoked or has expired.
    - When this is thorwn, all the relevant auth cookies are cleared by this function call, so you can redirect the user to a login page.
##### Additional information
- It does nothing to synchronize with other ```get_session_info``` or ```update_session_info``` calls on this session. So it is up to you to handle various race conditions depending on your use case. 

<div class="divider"></div>

## ```session.update_session_info(info)```
##### Parameters
- ```data```
    - Type: ```object | array | number | string | boolean | None``` 
##### Returns
- nothing
##### Throws
- ```SuperTokensGeneralException```
    - Examples of when this is thorwn is if the library could not connect to the database.
- ```SuperTokensUnauthorizedException```
    - This is thorwn if the current session was revoked or has expired.
    - When this is thorwn, all the relevant auth cookies are cleared by this function call, so you can redirect the user to a login page.
##### Additional information
- It does nothing to synchronize with other ```get_session_info``` or ```update_session_info``` calls on this session. So it is up to you to handle various race conditions depending on your use case. 

<div class="divider"></div>

## ```refresh_session(request, response)```
##### Parameters
- ```request```
    - Type: request parameter that is available in your view function (e.g. ```django.http.HttpRequest```)
- ```response```
    - Type: ```Response``` from ```rest_framework.response``` or you can also use ```HttpResponse``` from ```django.http``` or any response method which is extended from HttpResponse
##### Returns
- ```Session``` on successful refresh.
##### Throws
- ```SuperTokensGeneralException```
    - Examples of when this is thorwn is if the library could not connect to the MySQL instance.
- ```SuperTokensUnauthorizedException```
    - This is thorwn if the current session was revoked or has expired, or if the provided refresh token is invalid.
    - When this is thorwn, all the relevant auth cookies are cleared by this function call, so you can redirect the user to a login page.
- ```SuperTokensTokenTheftException```
    - This is thorwn if token theft is detected.
    - When this is thorwn, all the relevant auth cookies are cleared by this function call, so you can redirect the user to a login page.
    - If you are handling this exception, you'll have two functions on the exception object: get_user_id() and get_session_handle() to get user_id and session_handle for which token theft was detected
    - Please see the token theft detection section for more information.

<div class="divider"></div>

## ```get_session_info(session_handle)```
##### Parameters
- ```session_handle```
    - Type: ```string```
    - Identifies a unique session in your system. Please see the Session Handle section for more information.
##### Returnsof the resolved ```Promise``` will be deeply equal to whatever was passed to the ```create_new_session``` function.
##### Throws
- ```SuperTokensGeneralException```
    - Examples of when this is thorwn is if the library could not connect to the MySQL instance.
- ```SuperTokensUnauthorizedException```
    - This is thorwn if the current session was revoked or has expired.
    - You must handle auth cookie management yourself here (if relevant). Please see the Error Handling section for more details.
##### Additional information
- It does nothing to synchronize with other get_session_info or update_session_info calls on this ```session_handle```. So it is up to you to handle various race conditions depending on your use case.

<div class="divider"></div>

## ```update_session_info(session_handle, info)```
##### Parameters
- ```sessionHandle```
    - Type: ```string```
    - Identifies a unique session in your system. Please see the Session Handle section for more information.
- ```data```
    - Type: ```object | array | number | string | boolean | None``` 
##### Returns
- nothind
##### Throws
- ```SuperTokensGeneralException```
    - Examples of when this is thorwn is if the library could not connect to the MySQL instance.
- ```SuperTokensUnauthorizedException```
    - This is thorwn if the current session was revoked or has expired.
    - You must handle auth cookie management yourself here (if relevant). Please see the Error Handling section for more details.
##### Additional information
- It does nothing to synchronize with other get_session_info or update_session_info calls on this ```session_handle```. So it is up to you to handle various race conditions depending on your use case.

<div class="divider"></div>

## ```revoke_session(session_handle)```
##### Parameters
- ```session_handle```
    - Type: ```string```
    - Identifies a unique session in your system. Please see the Session Handle section for more information. 
##### Returns
- ```boolean```
    - Will be ```True``` if a row was removed from the database table.
    - Will be ```False``` if either the ```session_handle``` is invalid, or the session had already been removed.
##### Throws
- ```SuperTokensGeneralException```
    - Examples of when this is thorwn is if the library could not connect to the database.
##### Additional information
- This function deletes the session from the database
- If using blacklisting, this will immediately invalidate the JWT access token. If not, the user may still be able to continue using their access token to call authenticated APIs (until it expires).

<div class="divider"></div>

## ```revoke_all_sessions_for_user(user_id)```
##### Parameters
- ```user_id```
    - Type: ```string | number```
##### Returns
- nothing
##### Throws
- ```SuperTokensGeneralException```
    - Examples of when this is thorwn is if the library could not connect to the database.
##### Additional information
- This function deletes many sessions from the database. If it throws an error, then some sessions may already have been deleted.
- If using blacklisting, this will immediately invalidate the JWT access tokens associated with those sessions. If not, the user may still be able to continue using their access token to call authenticated APIs (until it expires).

<div class="divider"></div>

## ```get_all_session_handles_for_user(user_id)```
##### Parameters
- ```user_id```
    - Type: ```string | number```
##### Returns
- ```string[]```
    - Each element in the ```string[]``` is a ```session_handle```
##### Throws
- ```SuperTokensGeneralException```
    - Examples of when this is thorwn is if the library could not connect to the database.

<div class="divider"></div>

## ```set_headers_for_options_api(response)```
##### Parameters
- ```response```
    - Type: ```Response``` from ```rest_framework.response``` or you can also use ```HttpResponse``` from ```django.http``` or any response method which is extended from HttpResponse
##### Returns
- nothing
##### Throws
- ```SuperTokensGeneralException```
    - Examples of when this is thorwn is if something went wrong while setting headers.