from datetime import datetime, timedelta
from .models import SigningKey
from django.db import transaction
from .constant import ACCESS_TOKEN_SIGNING_KEY_NAME_IN_DB
from .utils import generate_new_signing_key, get_timezone
from .exceptions import raise_general_exception
from os import environ


class AccessTokenSigningKey:
    __instance = None

    @staticmethod
    def __get_instance():
        if AccessTokenSigningKey.__instance is None:
            AccessTokenSigningKey.__instance = AccessTokenSigningKey()
        return AccessTokenSigningKey.__instance

    def __init__(self):
        from .settings import supertokens_settings, get_access_token_signing_key_update_interval
        self.is_dynamic = supertokens_settings.ACCESS_TOKEN_SIGNING_KEY_IS_DYNAMIC
        self.update_interval = timedelta(
            seconds=get_access_token_signing_key_update_interval())
        self.user_get_key = supertokens_settings.ACCESS_TOKEN_SIGNING_KEY_GET_FUNCTION
        self.key = None
        self.created_at = None

    @staticmethod
    def get_key():
        return AccessTokenSigningKey.__get_instance().__get_key_from_instance()

    def __get_key_from_instance(self):
        if self.user_get_key is not None:
            try:
                return self.user_get_key()
            except Exception as e:
                raise_general_exception(
                    'Exception thrown from user provided function to get access token signing key', e)

        if self.key is None:
            new_key = self.__generate_new_key()
            self.key = new_key["key_value"]
            self.created_at = new_key["created_at"]

        current_datetime = datetime.now(tz=get_timezone())

        if self.is_dynamic and current_datetime > (self.created_at + self.update_interval):
            new_key = self.__generate_new_key()
            self.key = new_key["key_value"]
            self.created_at = new_key["created_at"]

        return self.key

    def __generate_new_key(self):
        try:
            with transaction.atomic():
                try:
                    key = SigningKey.objects.select_for_update().get(
                        key_name=ACCESS_TOKEN_SIGNING_KEY_NAME_IN_DB)
                except SigningKey.DoesNotExist:
                    key = None
                generate_new = False

                if key is not None:
                    current_datetime = datetime.now(tz=get_timezone())
                    if self.is_dynamic and current_datetime > (key.created_at + self.update_interval):
                        generate_new = True

                if key is None or generate_new:
                    key_value = generate_new_signing_key()
                    created_at = datetime.now(tz=get_timezone())
                    key = {
                        "key_value": key_value,
                        "created_at": created_at
                    }
                    SigningKey.objects.update_or_create(
                        key_name=ACCESS_TOKEN_SIGNING_KEY_NAME_IN_DB,
                        defaults={
                            "key_value": key_value,
                            "created_at": created_at
                        }
                    )
                else:
                    key = {
                        "key_value": key.key_value,
                        "created_at": key.created_at
                    }
            return key
        except Exception as e:
            raise_general_exception(e)

    @staticmethod
    def remove_key_from_memory():
        if AccessTokenSigningKey.__instance is not None:
            AccessTokenSigningKey.__instance.__remove_key_from_instance()

    def __remove_key_from_instance(self):
        self.created_at = None
        self.key = None

    @staticmethod
    def reset_instance():
        if environ.get("SUPERTOKENS_MODE", "dev") != "testing":
            raise_general_exception(
                'function should only be called during testing')
        SigningKey.objects.filter(
            key_name=ACCESS_TOKEN_SIGNING_KEY_NAME_IN_DB).delete()
        AccessTokenSigningKey.__instance = None
