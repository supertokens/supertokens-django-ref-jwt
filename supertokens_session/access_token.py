from .access_token_singingkey import AccessTokenSigningKey
from .jwt import encode, decode
from .utils import sanitize_string, sanitize_number
from datetime import datetime, timedelta
from math import floor
from .exceptions import raise_general_exception, raise_try_refresh_roken_exception

class AccessToken:
    
    @staticmethod
    def get_info_from_access_token(token, retry=True):
        from .settings import supertokens_settings

        signingkey = AccessTokenSigningKey.get_key()
        try:
            try:
                payload = decode(token, signingkey)
            except Exception as e:
                if retry:
                    AccessTokenSigningKey.remove_key_from_memory()
                    return AccessToken.get_info_from_access_token(token, False)
                else:
                    raise e
            session_handle = sanitize_string(payload["sessionHandle"])
            user_id = payload["userId"]
            refresh_token_hash_1 = sanitize_string(payload["rt"])
            expires_at = sanitize_number(payload["expiryTime"])
            if "prt" in payload:
                parent_refresh_token_hash_1 = sanitize_string(payload["prt"])
            else:
                parent_refresh_token_hash_1 = None
            if "antiCsrfToken" in payload:
                anti_csrf_token = sanitize_string(payload["antiCsrfToken"])
            else:
                anti_csrf_token = None
            if "userPayload" in payload:
                user_payload = payload["userPayload"]
            else:
                user_payload = None
            
            if session_handle is None or user_id is None or refresh_token_hash_1 is None or expires_at is None or (anti_csrf_token is None and supertokens_settings.ANTI_CSRF_ENABLE):
                raise Exception("invalid access token payload")

            current_datetime = datetime.now()
            expiry_datetime = datetime.fromtimestamp(expires_at)

            if expiry_datetime < current_datetime:
                raise Exception("expired access token")

            return {
                "user_id": user_id,
                "user_payload": user_payload,
                "expires_at": floor(expiry_datetime.timestamp()),
                "session_handle": session_handle,
                "anti_csrf_token": anti_csrf_token,
                "refresh_token_hash_1": refresh_token_hash_1,
                "parent_refresh_token_hash_1": parent_refresh_token_hash_1
            }
        except Exception as e:
            raise_try_refresh_roken_exception(e)

    @staticmethod
    def create_new_access_token(session_handle, user_id, refresh_token_hash_1, anti_csrf_token, parent_refresh_token_hash_1, user_payload):
        from .settings import supertokens_settings
        
        signingkey = AccessTokenSigningKey.get_key()
        try:
            validity = timedelta(seconds=supertokens_settings.ACCESS_TOKEN_VALIDITY)
            current_datetime = datetime.now()
            expires_at = validity + current_datetime
            expires_at = floor(expires_at.timestamp())
            token = encode({
                'sessionHandle': session_handle,
                'userId': user_id,
                'rt': refresh_token_hash_1,
                'antiCsrfToken': anti_csrf_token,
                'prt': parent_refresh_token_hash_1,
                'userPayload': user_payload,
                'expiryTime': expires_at
            }, signingkey)
            return {
                "token": token,
                "expires_at": expires_at
            }
        except Exception as e:
            raise_general_exception(e)