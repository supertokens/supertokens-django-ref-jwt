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
    return request.META.get(key.upper())

def get_cookie(request, key):
    return request.COOKIES[key]

def set_cookie(response, key, value, expires, path, domain, secure, httponly):
    response.set_cookie(key=key, value=value, expires=expires, path=path, domain=domain, secure=secure, httponly=httponly)