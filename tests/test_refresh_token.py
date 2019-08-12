from django.test import TestCase
from supertokens_session.refresh_token import RefreshToken
from supertokens_session.refresh_token_signing_key import RefreshTokenSigningKey
from .utils import set_default_settings, update_settings
from supertokens_session.exceptions import SuperTokensUnauthorizedException

class RefreshTokenTest(TestCase):

    def setUp(self):
        set_default_settings()
        RefreshTokenSigningKey.reset_instance()
    
    def test_create_and_get_RT(self):
        session_handle = 'sessionHandle'
        user_id = 'userId'
        parent_refresh_token_hash_1 = 'prt'
        token = RefreshToken.create_new_refresh_token(session_handle, user_id, parent_refresh_token_hash_1)
        token_info = RefreshToken.get_info_from_refresh_token(token["token"])
        self.assertEqual({
            "user_id": user_id,
            "session_handle": session_handle,
            "parent_refresh_token_hash_1": parent_refresh_token_hash_1
        }, token_info)
    
    def test_create_and_get_RT_different_keys(self):
        session_handle = 'sessionHandle'
        user_id = 'userId'
        parent_refresh_token_hash_1 = 'prt'
        token = RefreshToken.create_new_refresh_token(session_handle, user_id, parent_refresh_token_hash_1)
        RefreshTokenSigningKey.reset_instance()
        try:
            token_info = RefreshToken.get_info_from_refresh_token(token["token"])
            self.assertTrue(False)
        except SuperTokensUnauthorizedException as e:
            self.assertTrue(True)
        except Exception as e:
            self.assertTrue(False)