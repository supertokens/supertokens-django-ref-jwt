from supertokens_session.settings import reload_supertokens_settings


def set_default_settings():
    update_settings({})


def update_settings(value):
    reload_supertokens_settings(setting="SUPER_TOKENS", value=value)
