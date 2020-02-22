from .constant import (
    ACCESS_TOKEN_COOKIE_KEY,
    REFRESH_TOKEN_COOKIE_KEY,
    ID_REFRESH_TOKEN_COOKIE_KEY,
    ANTI_CSRF_HEADER_SET_KEY,
    ANTI_CSRF_HEADER_GET_KEY,
    ID_REFRESH_TOKEN_HEADER_GET_KEY,
    ID_REFRESH_TOKEN_HEADER_SET_KEY,
    SUPERTOKENS_SDK_NAME_HEADER_GET_KEY,
    SUPERTOKENS_SDK_NAME_HEADER_SET_KEY,
    SUPERTOKENS_SDK_VERSION_HEADER_GET_KEY,
    SUPERTOKENS_SDK_VERSION_HEADER_SET_KEY
)
from .exceptions import raise_general_exception
from datetime import datetime
from .utils import get_timezone


def set_options_api_headers(response):
    set_header(response, 'Access-Control-Allow-Headers', ANTI_CSRF_HEADER_SET_KEY)
    set_header(response, "Access-Control-Allow-Headers", SUPERTOKENS_SDK_NAME_HEADER_SET_KEY)
    set_header(response, "Access-Control-Allow-Headers", SUPERTOKENS_SDK_VERSION_HEADER_SET_KEY)
    set_header(response, 'Access-Control-Allow-Credentials', 'true')


def set_header(response, key, value):
    if response.has_header(key):
        existing_value = response.get(key)
        value = existing_value + ", " + value
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
    response.set_cookie(key=key, value=value, expires=datetime.fromtimestamp(
        expires, tz=get_timezone()), path=path, domain=domain, secure=secure, httponly=httponly)


def attach_anti_csrf_header_if_required(response, value):
    from .settings import supertokens_settings
    if supertokens_settings.ANTI_CSRF_ENABLE:
        if value is None:
            raise_general_exception(
                'BUG: anti-csrf token is null. if you are getting this error, please report this as a bug')
        set_header(response, ANTI_CSRF_HEADER_SET_KEY, value)
        set_header(response, 'Access-Control-Expose-Headers',
                   ANTI_CSRF_HEADER_SET_KEY)


def get_anti_csrf_header(request):
    return get_header(request, ANTI_CSRF_HEADER_GET_KEY)


def clear_session_from_cookie(response):
    from .settings import supertokens_settings
    set_cookie(response, ACCESS_TOKEN_COOKIE_KEY, '', 0, supertokens_settings.ACCESS_TOKEN_PATH,
               supertokens_settings.COOKIE_DOMAIN, supertokens_settings.COOKIE_SECURE, True)
    set_cookie(response, ID_REFRESH_TOKEN_COOKIE_KEY, '', 0,
               supertokens_settings.ACCESS_TOKEN_PATH, supertokens_settings.COOKIE_DOMAIN, False, False)
    set_cookie(response, REFRESH_TOKEN_COOKIE_KEY, '', 0, supertokens_settings.REFRESH_TOKEN_PATH,
               supertokens_settings.COOKIE_DOMAIN, supertokens_settings.COOKIE_SECURE, True)
    set_header(response, ID_REFRESH_TOKEN_HEADER_SET_KEY, "remove")
    set_header(response, "Access-Control-Expose-Headers", ID_REFRESH_TOKEN_HEADER_SET_KEY)


def attach_access_token_to_cookie(response, token, expires_at):
    from .settings import supertokens_settings
    set_cookie(response, ACCESS_TOKEN_COOKIE_KEY, token, expires_at, supertokens_settings.ACCESS_TOKEN_PATH,
               supertokens_settings.COOKIE_DOMAIN, supertokens_settings.COOKIE_SECURE, True)


def attach_refresh_token_to_cookie(response, token, expires_at):
    from .settings import supertokens_settings
    set_cookie(response, REFRESH_TOKEN_COOKIE_KEY, token, expires_at, supertokens_settings.REFRESH_TOKEN_PATH,
               supertokens_settings.COOKIE_DOMAIN, supertokens_settings.COOKIE_SECURE, True)


def attach_id_refresh_token_to_cookie_and_header(response, token, expires_at):
    from .settings import supertokens_settings
    set_cookie(response, ID_REFRESH_TOKEN_COOKIE_KEY, token, expires_at,
               supertokens_settings.ACCESS_TOKEN_PATH, supertokens_settings.COOKIE_DOMAIN, False, False)


def get_access_token_from_cookie(request):
    return get_cookie(request, ACCESS_TOKEN_COOKIE_KEY)


def get_refresh_token_from_cookie(request):
    return get_cookie(request, REFRESH_TOKEN_COOKIE_KEY)


def get_id_refresh_token_from_cookie(request):
    return get_cookie(request, ID_REFRESH_TOKEN_COOKIE_KEY)
