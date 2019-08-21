from . import session_helper
from .cookie_and_header import clear_session_from_cookie
from .exceptions import (
    SuperTokensUnauthorizedException,
)


class Session:
    def __init__(self, session_handle, user_id, jwt_payload, response):
        self.__session_handle = session_handle
        self.__user_id = user_id
        self.__jwt_payload = jwt_payload
        self.__response = response

    def revoke_session(self):
        if session_helper.revoke_session(self.__session_handle):
            clear_session_from_cookie(self.__response)

    def get_session_info(self):
        try:
            return session_helper.get_session_info(self.__session_handle)
        except SuperTokensUnauthorizedException as e:
            clear_session_from_cookie(self.__response)
            raise e

    def update_session_info(self, new_session_info):
        try:
            return session_helper.update_session_info(self.__session_handle, new_session_info)
        except SuperTokensUnauthorizedException as e:
            clear_session_from_cookie(self.__response)
            raise e

    def get_user_id(self):
        return self.__user_id

    def get_jwt_payload(self):
        return self.__jwt_payload
