from django.conf import settings
from rest_framework.settings import APISettings
from django.test.signals import setting_changed

# get settings from user
USER_SETTINGS = getattr(settings, "SUPER_TOKENS", None)

# default settings
DEFAULTS = {
    "ACCESS_TOKEN_SIGNING_KEY_IS_DYNAMIC": True,
    "ACCESS_TOKEN_SIGNING_KEY_UPDATE_INTERVAL": 24,
    "ACCESS_TOKEN_SIGNING_KEY_GET_FUNCTION": None,
    "ACCESS_TOKEN_VALIDITY": 3600,
    "ACCESS_TOKEN_ENABLE_BLACKLISTING": False,
    "ACCESS_TOKEN_PATH": "/",
    "ANTI_CSRF_ENABLE": True,
    "REFRESH_TOKEN_VALIDITY": 2400,
    "REFRESH_TOKEN_PATH": "refresh/",
    "COOKIE_DOMAIN": "localhost",
    "COOKIE_SECURE": True
}

supertokens_settings = APISettings(USER_SETTINGS, DEFAULTS)


def get_access_token_signing_key_update_interval():
    return supertokens_settings.ACCESS_TOKEN_SIGNING_KEY_UPDATE_INTERVAL * 60 * 60


def get_refresh_token_validity():
    return supertokens_settings.REFRESH_TOKEN_VALIDITY * 60 * 60


def reload_supertokens_settings(*args, **kwargs):  # pragma: no cover
    global supertokens_settings

    setting, value = kwargs['setting'], kwargs['value']

    if setting == 'SUPER_TOKENS':
        supertokens_settings = APISettings(value, DEFAULTS)


setting_changed.connect(reload_supertokens_settings)
