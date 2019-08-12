from .constant import (
    ACCESS_TOKEN_COOKIE_KEY,
    REFRESH_TOKEN_COOKIE_KEY,
    ID_REFRESH_TOKEN_COOKIE_KEY,
    ANTI_CSRF_HEADER_KEY
)
from .exceptions import raise_general_exception
from datetime import datetime

def set_options_api_headers(response):
    set_header(response, 'ACCESS-CONTROL-ALLOW-HEADERS', ANTI_CSRF_HEADER_KEY)
    set_header(response, 'ACCESS-CONTROL-ALLOW-CREDENTIALS', 'true')

def set_header(response, key, value):
    response[key] = value

def get_header(request, key):
    # though request.headers method is available, sticking to META because request.headers
    # is available only from django v2.2 which is the latest one and many might not be using this version
    # also, any HTTP header in the request are converted to META keys by converting all characters
    # to uppercase, replacing any hyphens with underscores and adding an HTTP_ prefix to the name.
    # e.g. a header called test-abc would be mapped to the META key HTTP_TEST_ABC
    # also, as a side note, request.headers provides access to all HTTP-prefixed headers (plus
    # Content-Length and Content-Type) from the request  
    return request.META.get('HTTP_' + key.upper())

def get_cookie(request, key):
    return request.COOKIES[key]

def set_cookie(response, key, value, expires, path, domain, secure, httponly):
    response.set_cookie(key=key, value=value, expires=datetime.fromtimestamp(expires), path=path, domain=domain, secure=secure, httponly=httponly)

def attach_anti_csrf_header_if_required(response, value):
    from .settings import supertokens_settings
    if supertokens_settings.ANTI_CSRF_ENABLE:
        if value == None:
            raise_general_exception('BUG: anti-csrf token is null. if you are getting this error, please report this as a bug')
        set_header(response, ANTI_CSRF_HEADER_KEY, value)
        set_header(response, 'ACCESS-CONTROL-EXPOSE-HEADERS', ANTI_CSRF_HEADER_KEY)

def get_anti_csrf_header(request):
    return get_header(request, ANTI_CSRF_HEADER_KEY)

def clear_session_from_cookie(response):
    from .settings import supertokens_settings
    set_cookie(response, ACCESS_TOKEN_COOKIE_KEY, '',  0, supertokens_settings.ACCESS_TOKEN_PATH, supertokens_settings.COOKIE_DOMAIN, supertokens_settings.COOKIE_SECURE, True)
    set_cookie(response, ID_REFRESH_TOKEN_COOKIE_KEY, '',  0, supertokens_settings.ACCESS_TOKEN_PATH, supertokens_settings.COOKIE_DOMAIN, False, False)
    set_cookie(response, REFRESH_TOKEN_COOKIE_KEY, '',  0, supertokens_settings.REFRESH_TOKEN_PATH, supertokens_settings.COOKIE_DOMAIN, supertokens_settings.COOKIE_SECURE, True)

def attach_access_token_to_cookie(response, token, expires_at):
    from .settings import supertokens_settings
    set_cookie(response, ACCESS_TOKEN_COOKIE_KEY, token,  expires_at, supertokens_settings.ACCESS_TOKEN_PATH, supertokens_settings.COOKIE_DOMAIN, supertokens_settings.COOKIE_SECURE, True)

def attach_refresh_token_to_cookie(response, token, expires_at):
    from .settings import supertokens_settings
    set_cookie(response, REFRESH_TOKEN_COOKIE_KEY, token,  expires_at, supertokens_settings.REFRESH_TOKEN_PATH, supertokens_settings.COOKIE_DOMAIN, supertokens_settings.COOKIE_SECURE, True)

def attach_id_refresh_token_to_cookie(response, token, expires_at):
    from .settings import supertokens_settings
    set_cookie(response, ID_REFRESH_TOKEN_COOKIE_KEY, token,  expires_at, supertokens_settings.ACCESS_TOKEN_PATH, supertokens_settings.COOKIE_DOMAIN, False, False)

def get_access_token_from_cookie(request):
    return get_cookie(request, ACCESS_TOKEN_COOKIE_KEY)

def get_refresh_token_from_cookie(request):
    return get_cookie(request, REFRESH_TOKEN_COOKIE_KEY)

def get_id_refresh_token_from_cookie(request):
    return get_cookie(request, ID_REFRESH_TOKEN_COOKIE_KEY)