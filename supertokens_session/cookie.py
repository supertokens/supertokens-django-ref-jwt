from .constant import (
    ACCESS_TOKEN_COOKIE_KEY,
    REFRESH_TOKEN_COOKIE_KEY,
    ID_REFRESH_TOKEN_COOKIE_KEY,
    ANTI_CSRF_HEADER_KEY
)
def set_options_api(response):
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
    response.set_cookie(key=key, value=value, expires=expires, path=path, domain=domain, secure=secure, httponly=httponly)