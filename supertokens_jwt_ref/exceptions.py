def raise_general_exception(msg, previous=None):
    if isinstance(msg, SuperTokensException):
        raise msg
    elif isinstance(msg, Exception):
        raise SuperTokensGeneralException(msg) from None
    raise SuperTokensGeneralException(msg) from previous


def raise_token_theft_exception(user_id, session_handle):
    raise SuperTokensTokenTheftException(user_id, session_handle)


def raise_try_refresh_token_exception(msg):
    if isinstance(msg, SuperTokensException):
        raise msg
    raise SuperTokensTryRefreshTokenException(msg) from None


def raise_unauthorized_exception(msg):
    if isinstance(msg, SuperTokensException):
        raise msg
    raise SuperTokensUnauthorizedException(msg) from None


class SuperTokensException(Exception):
    pass


class SuperTokensGeneralException(SuperTokensException):
    pass


class SuperTokensTokenTheftException(SuperTokensException):
    def __init__(self, user_id, session_handle):
        super().__init__('token theft detected')
        self.user_id = user_id
        self.session_handle = session_handle

    def get_user_id(self):
        return self.user_id

    def get_session_handle(self):
        return self.session_handle


class SuperTokensUnauthorizedException(SuperTokensException):
    pass


class SuperTokensTryRefreshTokenException(SuperTokensException):
    pass
