from datetime import datetime
from .models import SigningKey
from django.db import transaction
from .constant import REFRESH_TOKEN_KEY_NAME_IN_DB
from .utils import generate_new_signing_key
from .exceptions import raise_general_exception
from os import environ

class RefreshTokenSigningKey:
    __instance = None

    @staticmethod
    def get_instance():
        if RefreshTokenSigningKey.__instance == None:
            RefreshTokenSigningKey.__instance = RefreshTokenSigningKey()
        return RefreshTokenSigningKey.__instance

    def __init__(self):
        self.key = None

    @staticmethod
    def get_key():
        return RefreshTokenSigningKey.get_instance().__get_key_from_instance()

    def __get_key_from_instance(self):
        if self.key is None:
            self.key = self.__generate_new_key()
        return self.key
    
    def __generate_new_key(self):
        try:
            with transaction.atomic():
                try:
                    key = SigningKey.objects.select_for_update().get(key_name=REFRESH_TOKEN_KEY_NAME_IN_DB)
                except SigningKey.DoesNotExist as e:
                    key = None
                generate_new = False
                
                if key == None or generate_new:
                    key_value = generate_new_signing_key()
                    created_at = datetime.now()
                    key = key_value
                    SigningKey.objects.update_or_create(
                        key_name=REFRESH_TOKEN_KEY_NAME_IN_DB,
                        defaults= {
                            "key_value": key_value,
                            "created_at": created_at
                        }
                    )
                else:
                    key = key.key_value
            return key
        except Exception as e:
            raise_general_exception(e)
    
    @staticmethod
    def reset_instance():
        if environ.get("SUPERTOKENS_MODE", "dev") != "testing":
            raise_general_exception('function should only be called during testing')
        SigningKey.objects.filter(key_name=REFRESH_TOKEN_KEY_NAME_IN_DB).delete()
        RefreshTokenSigningKey.__instance = None