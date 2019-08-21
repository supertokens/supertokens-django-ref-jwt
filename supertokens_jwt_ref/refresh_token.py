from .refresh_token_signing_key import RefreshTokenSigningKey
from .utils import encrypt, decrypt, sanitize_string, generate_uuid, custom_hash, get_timezone, sanitize_number
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
            user_id = sanitize_number(payload["userId"])
            if user_id is None:
                user_id = sanitize_string(payload["userId"])
            parent_refresh_token_hash_1 = sanitize_string(payload["prt"])
            nonce_from_token = sanitize_string(payload["nonce"])

            if session_handle is None or user_id is None or nonce_from_token != nonce:
                raise Exception("invalid refresh token")

            return {
                "session_handle": session_handle,
                "user_id": user_id,
                "parent_refresh_token_hash_1": parent_refresh_token_hash_1
            }
        except Exception as e:
            raise_unauthorized_exception(e)

    @staticmethod
    def create_new_refresh_token(session_handle, user_id, parent_refresh_token_hash_1):
        key = RefreshTokenSigningKey.get_key()

        try:
            nonce = custom_hash(generate_uuid())
            serialized_payload = dumps({
                "sessionHandle": session_handle,
                "userId": user_id,
                "prt": parent_refresh_token_hash_1,
                "nonce": nonce,
            })
            encrypted_part = encrypt(serialized_payload, key)
            token = encrypted_part + "." + nonce
            validity = RefreshToken.get_validity()
            current_datetime = datetime.now(tz=get_timezone())
            expires_at = validity + current_datetime
            expires_at = floor(expires_at.timestamp())
            return {
                "token": token,
                "expires_at": expires_at
            }
        except Exception as e:
            raise_general_exception(e)

    @staticmethod
    def get_validity():
        from .settings import get_refresh_token_validity
        return timedelta(seconds=get_refresh_token_validity())
