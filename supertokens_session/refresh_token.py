from .refresh_token_signing_key import RefreshTokenSigningKey
from .utils import encrypt, decrypt, sanitize_string, generate_uuid
from json import dumps, loads
from datetime import datetime, timedelta
from math import floor
from .exceptions import raise_general_exception, raise_unauthorized_exception

class RefreshToken:

    @staticmethod
    def get_info_from_refresh_token(token):
        key = RefreshTokenSigningKey.get_key()

        try:
            splitted_token = token.split(".")

            if len(splitted_token) > 2:
                raise Exception("invalid refresh token")
            
            nonce = splitted_token[1]
            payload = loads(decrypt(splitted_token[0], key))
            session_handle = sanitize_string(payload["sessionHandle"])
            user_id = payload["userId"]
            parent_refresh_token_hash_1 = sanitize_string(payload["prt"])
            nonce_from_token = sanitize_string(payload["nonce"])

            if session_handle is None or user_id is None or nonce_from_token != nonce:
                raise Exception("invalid refresh token")

            return {
                "user_id": user_id,
                "session_handle": session_handle,
                "parent_refresh_token_hash_1": parent_refresh_token_hash_1
            }
        except Exception as e:
            raise_unauthorized_exception(e)

    @staticmethod
    def create_new_refresh_token(session_handle, user_id, parent_refresh_token_hash_1):
        key = RefreshTokenSigningKey.get_key()

        try:
            nonce = generate_uuid()
            serialized_payload = dumps({
                "nonce": nonce,
                "userId": user_id,
                "sessionHandle": session_handle,
                "prt": parent_refresh_token_hash_1
            })
            encrypted_part = encrypt(serialized_payload, key)
            token = encrypted_part + "." + nonce
            validity = RefreshToken.get_validity()
            current_datetime = datetime.now()
            expires_at = current_datetime + validity
            return {
                "token": token,
                "expires_at": floor(expires_at.timestamp())
            }
        except Exception as e:
            raise_general_exception(e)
    
    @staticmethod
    def get_validity():
        from .settings import supertokens_settings
        return timedelta(seconds=supertokens_settings.REFRESH_TOKEN_VALIDITY * 60 * 60)
