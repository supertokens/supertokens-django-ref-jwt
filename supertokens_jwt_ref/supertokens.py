from .cookie_and_header import (
    get_anti_csrf_header,
    set_options_api_headers,
    clear_session_from_cookie,
    get_access_token_from_cookie,
    attach_access_token_to_cookie,
    get_refresh_token_from_cookie,
    attach_refresh_token_to_cookie,
    get_id_refresh_token_from_cookie,
    attach_id_refresh_token_to_cookie_and_header,
    attach_anti_csrf_header_if_required
)
from .session import Session
from . import session_helper
from .exceptions import (
    raise_unauthorized_exception,
    SuperTokensTokenTheftException,
    SuperTokensUnauthorizedException,
    raise_try_refresh_token_exception
)


def create_new_session(response, user_id, jwt_payload=None, session_info=None):
    new_session = session_helper.create_new_session(
        user_id, jwt_payload, session_info)

    attach_access_token_to_cookie(
        response, new_session['access_token']['value'], new_session['access_token']['expires_at'])
    attach_refresh_token_to_cookie(
        response, new_session['refresh_token']['value'], new_session['refresh_token']['expires_at'])
    attach_id_refresh_token_to_cookie_and_header(
        response, new_session['id_refresh_token']['value'], new_session['id_refresh_token']['expires_at'])
    attach_anti_csrf_header_if_required(
        response, new_session['anti_csrf_token'])

    return Session(new_session['session']['handle'], new_session['session']['user_id'], new_session['session']['jwt_payload'], response)


def get_session(request, response, enable_csrf_protection):
    id_refresh_token = get_id_refresh_token_from_cookie(request)

    if id_refresh_token is None:
        clear_session_from_cookie(response)
        raise_unauthorized_exception('missing auth tokens in cookies')

    access_token = get_access_token_from_cookie(request)
    if access_token is None:
        raise_try_refresh_token_exception('access token missing in cookies')

    try:
        from .settings import supertokens_settings
        enable_csrf_protection = enable_csrf_protection and supertokens_settings.ANTI_CSRF_ENABLE
        anti_csrf_token = get_anti_csrf_header(
            request) if enable_csrf_protection else None

        if anti_csrf_token is None and enable_csrf_protection:
            raise_try_refresh_token_exception('anti csrf token is missing')
        session = session_helper.get_session(access_token, anti_csrf_token if anti_csrf_token is not None else False)
        if session['new_access_token'] is not None:
            attach_access_token_to_cookie(
                response, session['new_access_token']['value'], session['new_access_token']['expires_at'])
        return Session(session['session']['handle'], session['session']['user_id'], session['session']['jwt_payload'], response)
    except SuperTokensUnauthorizedException as e:
        clear_session_from_cookie(response)
        raise e


def refresh_session(request, response):
    refresh_token = get_refresh_token_from_cookie(request)
    id_refresh_token = get_id_refresh_token_from_cookie(request)

    if id_refresh_token is None or refresh_token is None:
        clear_session_from_cookie(response)
        raise_unauthorized_exception('missing auth tokens in cookies')

    try:
        new_session = session_helper.refresh_session(refresh_token)

        attach_access_token_to_cookie(
            response, new_session['new_access_token']['value'], new_session['new_access_token']['expires_at'])
        attach_refresh_token_to_cookie(
            response, new_session['new_refresh_token']['value'], new_session['new_refresh_token']['expires_at'])
        attach_id_refresh_token_to_cookie_and_header(
            response, new_session['new_id_refresh_token']['value'], new_session['new_id_refresh_token']['expires_at'])
        attach_anti_csrf_header_if_required(
            response, new_session['new_anti_csrf_token'])

        return Session(new_session['session']['handle'], new_session['session']['user_id'], new_session['session']['jwt_payload'], response)
    except SuperTokensUnauthorizedException as e:
        clear_session_from_cookie(response)
        raise e
    except SuperTokensTokenTheftException as e:
        clear_session_from_cookie(response)
        raise e


def revoke_all_sessions_for_user(user_id):
    session_helper.revoke_all_sessions_for_user(user_id)


def get_all_session_handles_for_user(user_id):
    return session_helper.get_all_session_handles_for_user(user_id)


def revoke_session(session_handle):
    return session_helper.revoke_session(session_handle)


def get_session_info(session_handle):
    return session_helper.get_session_info(session_handle)


def update_session_info(session_handle, new_session_info):
    return session_helper.update_session_info(session_handle, new_session_info)


def set_headers_for_options_api(response):
    set_options_api_headers(response)
