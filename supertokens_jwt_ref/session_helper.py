from .utils import (
    generate_uuid,
    custom_hash,
    get_timezone,
    serialize_data,
    unserialize_data,
    serialize_user_id,
    unserialize_user_id,
    assert_user_id_has_correct_format
)
from .refresh_token import RefreshToken
from .access_token import AccessToken
from .models import RefreshToken as RefreshTokenModel
from django.db import transaction
from datetime import datetime
from .exceptions import (
    raise_general_exception,
    raise_token_theft_exception,
    raise_unauthorized_exception,
    raise_try_refresh_token_exception
)


def create_new_session(user_id, jwt_payload, session_info):
    from .settings import supertokens_settings
    assert_user_id_has_correct_format(user_id)
    try:
        session_handle = generate_uuid()
        refresh_token = RefreshToken.create_new_refresh_token(
            session_handle, user_id, None)
        anti_csrf_token = generate_uuid() if supertokens_settings.ANTI_CSRF_ENABLE else None
        access_token = AccessToken.create_new_access_token(session_handle, user_id, custom_hash(
            refresh_token['token']), anti_csrf_token, None, jwt_payload)

        session_in_db = RefreshTokenModel(session_handle=session_handle, user_id=serialize_user_id(user_id), refresh_token_hash_2=custom_hash(custom_hash(
            refresh_token['token'])), session_info=serialize_data(session_info), expires_at=datetime.fromtimestamp(refresh_token['expires_at'], tz=get_timezone()), jwt_payload=serialize_data(jwt_payload))
        session_in_db.save()

        return {
            'session': {
                'handle': session_handle,
                'user_id': user_id,
                'jwt_payload': jwt_payload,
            },
            'access_token': {
                'value': access_token['token'],
                'expires_at': access_token['expires_at'],
            },
            'refresh_token': {
                'value': refresh_token['token'],
                'expires_at': refresh_token['expires_at'],
            },
            'id_refresh_token': {
                'value': generate_uuid(),
                'expires_at': refresh_token['expires_at'],
            },
            'anti_csrf_token': anti_csrf_token
        }
    except Exception as e:
        raise_general_exception(e)


# anti_csrf_token should be False if user does not want to have CSRF check for this API.
def get_session(access_token, anti_csrf_token):
    from .settings import supertokens_settings

    try:
        access_token_info = AccessToken.get_info_from_access_token(
            access_token)
        session_handle = access_token_info['session_handle']

        anti_csrf_token = anti_csrf_token if supertokens_settings.ANTI_CSRF_ENABLE else False
        if anti_csrf_token is None:
            raise_general_exception("provided antiCsrfToken is None. Please pass False instead")
        if anti_csrf_token is not False and anti_csrf_token != access_token_info['anti_csrf_token']:
            raise_try_refresh_token_exception("anti-csrf check failed")

        enable_blacklisting = supertokens_settings.ACCESS_TOKEN_ENABLE_BLACKLISTING

        if enable_blacklisting:
            is_session_handle_blacklisted = RefreshTokenModel.objects.filter(
                session_handle=session_handle).count() == 0
            if is_session_handle_blacklisted:
                raise_unauthorized_exception(
                    'session is over or has been blacklisted')

        if access_token_info['parent_refresh_token_hash_1'] is None:
            return {
                'session': {
                    'handle': access_token_info['session_handle'],
                    'user_id': access_token_info['user_id'],
                    'jwt_payload': access_token_info['user_payload']
                },
                'new_access_token': None
            }

        with transaction.atomic():
            session = __get_session_from_database_for_update(session_handle)
            promote_bool = session.refresh_token_hash_2 == custom_hash(
                access_token_info['parent_refresh_token_hash_1'])

            if promote_bool or session.refresh_token_hash_2 == custom_hash(access_token_info['refresh_token_hash_1']):
                if promote_bool:
                    refresh_token_validity = RefreshToken.get_validity()
                    current_datetime = datetime.now(tz=get_timezone())
                    expires_at = refresh_token_validity + current_datetime
                    RefreshTokenModel.objects.filter(session_handle=session_handle).update(
                        refresh_token_hash_2=custom_hash(access_token_info['refresh_token_hash_1']), expires_at=expires_at)

                new_access_token = AccessToken.create_new_access_token(
                    session_handle, access_token_info['user_id'], access_token_info['refresh_token_hash_1'], access_token_info['anti_csrf_token'], None, access_token_info['user_payload'])

                return {
                    'session': {
                        'handle': session_handle,
                        'user_id': access_token_info['user_id'],
                        'jwt_payload': access_token_info['user_payload']
                    },
                    'new_access_token': {
                        'value': new_access_token['token'],
                        'expires_at': new_access_token['expires_at']
                    }
                }

        raise_unauthorized_exception(
            'using access token whose refresh token is no more')
    except RefreshTokenModel.DoesNotExist:
        raise_unauthorized_exception('missing session in db')
    except Exception as e:
        raise_general_exception(e)


def refresh_session(refresh_token):
    refresh_token_info = RefreshToken.get_info_from_refresh_token(
        refresh_token)
    return refresh_session_helper(refresh_token, refresh_token_info)


def refresh_session_helper(refresh_token, refresh_token_info):
    session_handle = refresh_token_info['session_handle']
    try:
        with transaction.atomic():
            session = __get_session_from_database_for_update(session_handle)
            current_datetime = datetime.now(tz=get_timezone())
            if session.expires_at < current_datetime:
                raise_unauthorized_exception(
                    'session does not exist or is expired')
            if session.user_id != refresh_token_info['user_id']:
                raise_unauthorized_exception(
                    'user id for session does not match with the user id in the refresh token')

            if session.refresh_token_hash_2 == custom_hash(custom_hash(refresh_token)):
                from .settings import supertokens_settings
                new_refresh_token = RefreshToken.create_new_refresh_token(
                    session_handle, refresh_token_info['user_id'], custom_hash(refresh_token))
                new_anti_csrf_token = generate_uuid() if supertokens_settings.ANTI_CSRF_ENABLE else None
                new_access_token = AccessToken.create_new_access_token(session_handle, refresh_token_info['user_id'], custom_hash(
                    new_refresh_token['token']), new_anti_csrf_token, custom_hash(refresh_token), session.jwt_payload)

                return {
                    'session': {
                        'handle': session_handle,
                        'user_id': refresh_token_info['user_id'],
                        'jwt_payload': session.jwt_payload,
                    },
                    'new_access_token': {
                        'value': new_access_token['token'],
                        'expires_at': new_access_token['expires_at'],
                    },
                    'new_refresh_token': {
                        'value': new_refresh_token['token'],
                        'expires_at': new_refresh_token['expires_at'],
                    },
                    'new_id_refresh_token': {
                        'value': generate_uuid(),
                        'expires_at': new_refresh_token['expires_at'],
                    },
                    'new_anti_csrf_token': new_anti_csrf_token
                }

            if refresh_token_info['parent_refresh_token_hash_1'] is not None and custom_hash(refresh_token_info['parent_refresh_token_hash_1']) == session.refresh_token_hash_2:
                refresh_token_validity = RefreshToken.get_validity()
                current_datetime = datetime.now(tz=get_timezone())
                expires_at = refresh_token_validity + current_datetime
                RefreshTokenModel.objects.filter(session_handle=session_handle).update(
                    refresh_token_hash_2=custom_hash(custom_hash(refresh_token)), expires_at=expires_at)
                return refresh_session_helper(refresh_token, refresh_token_info)

        raise_token_theft_exception(
            refresh_token_info['user_id'], session_handle)
    except RefreshTokenModel.DoesNotExist:
        raise_unauthorized_exception('session does not exist or is expired')
    except Exception as e:
        raise_general_exception(e)


def revoke_all_sessions_for_user(user_id):
    try:
        RefreshTokenModel.objects.filter(
            user_id=serialize_user_id(user_id)).delete()
    except Exception as e:
        raise_general_exception(e)


def get_all_session_handles_for_user(user_id):
    try:
        sessions = RefreshTokenModel.objects.filter(
            user_id=serialize_user_id(user_id))
        session_handles = []
        for session in sessions:
            session_handles.append(session.session_handle)
            return session_handles
    except Exception as e:
        raise_general_exception(e)


def revoke_session(session_handle):
    try:
        # deletes the object and returns the number of objects deleted and a dictionary with the number of deletions per object type
        rows_deleted, _ = RefreshTokenModel.objects.get(
            session_handle=session_handle).delete()
        return rows_deleted == 1
    except RefreshTokenModel.DoesNotExist:
        return False
    except Exception as e:
        raise_general_exception(e)


def get_session_info(session_handle):
    try:
        session = __get_session_from_database(session_handle)
        return session.session_info
    except RefreshTokenModel.DoesNotExist:
        raise_unauthorized_exception("session does not exist anymore")
    except Exception as e:
        raise_general_exception(e)


def update_session_info(session_handle, session_info):
    try:
        RefreshTokenModel.objects.filter(
            session_handle=session_handle).update(session_info=serialize_data(session_info))
    except RefreshTokenModel.DoesNotExist:
        raise_unauthorized_exception('session does not exist anymore')
    except Exception as e:
        raise_general_exception(e)


def remove_expired_tokens():
    return RefreshTokenModel.objects.filter(expires_at__lte=datetime.now(tz=get_timezone())).delete()


def __get_session_from_database_for_update(session_handle):
    session = RefreshTokenModel.objects.select_for_update().get(
        session_handle=session_handle)
    session.user_id = unserialize_user_id(session.user_id)
    session.jwt_payload = unserialize_data(session.jwt_payload)
    session.session_info = unserialize_data(session.session_info)
    return session


def __get_session_from_database(session_handle):
    session = RefreshTokenModel.objects.get(session_handle=session_handle)
    session.user_id = unserialize_user_id(session.user_id)
    session.jwt_payload = unserialize_data(session.jwt_payload)
    session.session_info = unserialize_data(session.session_info)
    return session
