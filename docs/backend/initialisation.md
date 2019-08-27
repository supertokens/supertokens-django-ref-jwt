---
id: initialisation
title: Initialisation
sidebar_label: Setup
---

## Adding to Installed Apps
- Add package to INSTALLED_APPS in settings.py of your main app
```python
# Django project settings.py

INSTALLED_APPS = [
    ...,
    "supertokens_jwt_ref",
    ...
]
```

## Run make migrations
```bash
python manage.py makemigrations supertokens_jwt_ref
```

## Run migrate
```bash
python manage.py migrate supertokens_jwt_ref
```

## Configurations
Many configuration options are available for supertokens and can be configured by setting `SUPER_TOKENS` variable in `settings.py`:
```python
# Django project settings.py

...
SUPER_TOKENS = {
    "ACCESS_TOKEN_SIGNING_KEY_IS_DYNAMIC": True,
    # if this is true, then the JWT signing key will change automatically every updateInterval hours.
    
    "ACCESS_TOKEN_SIGNING_KEY_UPDATE_INTERVAL": 24,
    # in hours - should be >= 1 && <= 720. Determines how often to change the signing key. If dynamic is false, then this does not matter. 
    
    "ACCESS_TOKEN_SIGNING_KEY_GET_FUNCTION": None,
    # If you want to give your own JWT signing key, please give a function here. If this is given, then the dynamic boolean will be ignored as key management will be up to you. This function will be called every time we generate or verify any JWT, so please make sure it is efficient.
    
    "ACCESS_TOKEN_VALIDITY": 3600,
    # in seconds. Should ideally be >= 10 && <= 86400000 seconds. This determines the lifetime of an access token.
    
    "ACCESS_TOKEN_ENABLE_BLACKLISTING": False,
    # If you set this to true, revoking a session will cause immediate logout of the user using that session, regardless of access token's lifetime.
    
    "ACCESS_TOKEN_PATH": "/",
    # This will be the path of the access token cookie.
    
    "ANTI_CSRF_ENABLE": True,
    # When set to true, you will also get a custom CSRF attack protection. 
    
    "REFRESH_TOKEN_VALIDITY": 2400,
    # in hours. Should be >= 1 hour && <= 365 * 24 hours. This determines how long a refresh token is alive for.
    
    "REFRESH_TOKEN_PATH": "refresh/",
    # this is the API path that needs to be called for refreshing a session. This needs to be a POST API. An example value is "/api/refreshtoken". This will also be the path of the refresh token cookie.
    
    "COOKIE_DOMAIN": "localhost",
    # this is the domain to set for all the cookies. If using a website, please make sure this domain is the common part of your website domain and your API domain. Do not set any port here and do not put http:// or https:/
    
    "COOKIE_SECURE": True
    # Sets if the cookies are secure or not. If you do not have https, make this false.
}
```