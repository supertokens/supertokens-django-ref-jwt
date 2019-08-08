from django.test import TestCase
from django.conf import settings
from supertokens_session.access_token import AccessToken
from supertokens_session.access_token_singingkey import AccessTokenSigningKey
from .utils import set_default_settings, update_settings
from time import sleep
from supertokens_session.exceptions import SuperTokensTryRefreshTokenException

class AccessTokenTest(TestCase):

    def setUp(self):
        set_default_settings()
        AccessTokenSigningKey.reset_instance()
    
    def test_create_and_get_AT(self):
        session_handle = 'sessionHandle'
        user_id = 'userId'
        refresh_token_hash_1 = 'rt'
        anti_csrf_token = 'antiCsrfToken'
        parent_refresh_token_hash_1 = 'prt'
        user_payload = {'a': 'a'}
        token = AccessToken.create_new_access_token(session_handle, user_id, refresh_token_hash_1, anti_csrf_token, parent_refresh_token_hash_1, user_payload)
        token_info = AccessToken.get_info_from_access_token(token["token"])
        self.assertEqual({
            "session_handle": 'sessionHandle',
            "user_id": 'userId',
            "refresh_token_hash_1": 'rt',
            "anti_csrf_token": 'antiCsrfToken',
            "parent_refresh_token_hash_1": 'prt',
            "user_payload": {'a': 'a'},
            "expires_at": token["expires_at"]
        }, token_info)
    
    def test_custom_signingkey_function(self):
        def signingkey_func():
            return "test"
        new_settings = {
            "ACCESS_TOKEN_SIGNING_KEY_GET_FUNCTION": signingkey_func
        }
        update_settings(new_settings)
        self.assertEqual(AccessTokenSigningKey.get_key(), signingkey_func())
    
    def test_very_short_update_interval_for_signingkey(self):
        new_settings = {
            "ACCESS_TOKEN_SIGNING_KEY_UPDATE_INTERVAL": 0.0005
        }
        update_settings(new_settings)
        key1 = AccessTokenSigningKey.get_key()
        sleep(2)
        key2 = AccessTokenSigningKey.get_key()
        self.assertNotEqual(key1, key2)

    def test_create_and_get_AT_short_validity(self):
        new_settings = {
            "ACCESS_TOKEN_VALIDITY": 1
        }
        update_settings(new_settings)
        session_handle = 'sessionHandle'
        user_id = 'userId'
        refresh_token_hash_1 = 'rt'
        anti_csrf_token = 'antiCsrfToken'
        parent_refresh_token_hash_1 = 'prt'
        user_payload = {'a': 'a'}
        token = AccessToken.create_new_access_token(session_handle, user_id, refresh_token_hash_1, anti_csrf_token, parent_refresh_token_hash_1, user_payload)
        sleep(1.5)
        try:
            token_info = AccessToken.get_info_from_access_token(token["token"])
            self.assertTrue(False)
        except SuperTokensTryRefreshTokenException as e:
            self.assertTrue(True)
        except Exception as e:
            self.assertTrue(False)
    
    def test_create_and_get_AT_with_very_short_update_interval_for_signingkey(self):
        new_settings = {
            "ACCESS_TOKEN_SIGNING_KEY_UPDATE_INTERVAL": 0.0005
        }
        update_settings(new_settings)
        session_handle = 'sessionHandle'
        user_id = 'userId'
        refresh_token_hash_1 = 'rt'
        anti_csrf_token = 'antiCsrfToken'
        parent_refresh_token_hash_1 = 'prt'
        user_payload = {'a': 'a'}
        token = AccessToken.create_new_access_token(session_handle, user_id, refresh_token_hash_1, anti_csrf_token, parent_refresh_token_hash_1, user_payload)
        sleep(2)
        try:
            token_info = AccessToken.get_info_from_access_token(token["token"])
            self.assertTrue(False)
        except SuperTokensTryRefreshTokenException as e:
            self.assertTrue(True)
        except Exception as e:
            self.assertTrue(False)