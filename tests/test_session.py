from django.test import TestCase
from supertokens_jwt_ref.session_helper import (
    revoke_all_sessions_for_user,
    remove_expired_tokens,
    update_session_info,
    create_new_session,
    get_session_info,
    refresh_session,
    revoke_session,
    get_session
)
from supertokens_jwt_ref.refresh_token_signing_key import RefreshTokenSigningKey
from supertokens_jwt_ref.access_token_singingkey import AccessTokenSigningKey
from supertokens_jwt_ref.models import RefreshToken as RefreshTokenModel
from supertokens_jwt_ref.utils import base64encode
from .utils import set_default_settings, update_settings
from .schema import (
    schema_new_session_get,
    schema_refresh_session_ACT_enabled,
    schema_refresh_session_ACT_disabled,
    schema_create_new_session_ACT_enabled,
    schema_create_new_session_ACT_disabled,
    schema_updated_access_token_session_get
)
from jsonschema import validate
from time import sleep
from json import dumps
from supertokens_jwt_ref.exceptions import (
    SuperTokensTokenTheftException,
    SuperTokensUnauthorizedException,
    SuperTokensTryRefreshTokenException
)


class SessionTest(TestCase):

    def setUp(self):
        set_default_settings()
        AccessTokenSigningKey.reset_instance()
        RefreshTokenSigningKey.reset_instance()

    def test_create_and_get_session_ACT_enabled(self):
        user_id = 'userId'
        jwt_payload = {'a': 'a'}
        session_data = {'b': 'b'}

        session = create_new_session(user_id, jwt_payload, session_data)
        validate(session, schema_create_new_session_ACT_enabled)
        self.assertEqual(session['session']['user_id'], user_id)
        self.assertEqual(session['session']['jwt_payload'], jwt_payload)

        self.assertEqual(RefreshTokenModel.objects.all().count(), 1)

        session_info = get_session(
            session['access_token']['value'], session['anti_csrf_token'])
        validate(session_info, schema_new_session_get)
        self.assertEqual(session_info['session']['user_id'], user_id)
        self.assertEqual(session_info['session']['jwt_payload'], jwt_payload)

        session_info = get_session(session['access_token']['value'])
        validate(session_info, schema_new_session_get)
        self.assertEqual(session_info['session']['user_id'], user_id)
        self.assertEqual(session_info['session']['jwt_payload'], jwt_payload)

        try:
            get_session(session['access_token']['value'], 'some-random-string')
            self.assertTrue(False)
        except SuperTokensTryRefreshTokenException:
            self.assertTrue(True)

    def test_create_and_get_session_ACT_disabled(self):
        new_settings = {
            "ANTI_CSRF_ENABLE": False
        }
        update_settings(new_settings)

        user_id = 'userId'
        jwt_payload = {'a': 'a'}
        session_data = {'b': 'b'}

        session = create_new_session(user_id, jwt_payload, session_data)
        validate(session, schema_create_new_session_ACT_disabled)
        self.assertEqual(session['session']['user_id'], user_id)
        self.assertEqual(session['session']['jwt_payload'], jwt_payload)

        self.assertEqual(RefreshTokenModel.objects.all().count(), 1)

        session_info = get_session(session['access_token']['value'])
        validate(session_info, schema_new_session_get)
        self.assertEqual(session_info['session']['user_id'], user_id)
        self.assertEqual(session_info['session']['jwt_payload'], jwt_payload)

    def test_create_and_get_session_different_payload_types(self):
        user_id = 'userId'
        jwt_payload = 2
        session_data = 123

        session = create_new_session(user_id, jwt_payload, session_data)
        validate(session, schema_create_new_session_ACT_enabled)
        session_info = get_session(
            session['access_token']['value'], session['anti_csrf_token'])
        validate(session_info, schema_new_session_get)
        self.assertEqual(session_info['session']['jwt_payload'], jwt_payload)
        self.assertEqual(get_session_info(
            session_info['session']['handle']), session_data)

        jwt_payload = 'testing'
        session_data = 'supertokens'

        session = create_new_session(user_id, jwt_payload, session_data)
        validate(session, schema_create_new_session_ACT_enabled)
        session_info = get_session(
            session['access_token']['value'], session['anti_csrf_token'])
        validate(session_info, schema_new_session_get)
        self.assertEqual(session_info['session']['jwt_payload'], jwt_payload)
        self.assertEqual(get_session_info(
            session_info['session']['handle']), session_data)

        jwt_payload = True
        session_data = False

        session = create_new_session(user_id, jwt_payload, session_data)
        validate(session, schema_create_new_session_ACT_enabled)
        session_info = get_session(
            session['access_token']['value'], session['anti_csrf_token'])
        validate(session_info, schema_new_session_get)
        self.assertEqual(session_info['session']['jwt_payload'], jwt_payload)
        self.assertEqual(get_session_info(
            session_info['session']['handle']), session_data)

        jwt_payload = [1, 2, 3, 'a', 'b', 'c']
        session_data = [4, 5, 6, 'd', 'e', 'f']

        session = create_new_session(user_id, jwt_payload, session_data)
        validate(session, schema_create_new_session_ACT_enabled)
        session_info = get_session(
            session['access_token']['value'], session['anti_csrf_token'])
        validate(session_info, schema_new_session_get)
        self.assertEqual(session_info['session']['jwt_payload'], jwt_payload)
        self.assertEqual(get_session_info(
            session_info['session']['handle']), session_data)

        jwt_payload = None
        session_data = None

        session = create_new_session(user_id, jwt_payload, session_data)
        validate(session, schema_create_new_session_ACT_enabled)
        session_info = get_session(
            session['access_token']['value'], session['anti_csrf_token'])
        validate(session_info, schema_new_session_get)
        self.assertEqual(session_info['session']['jwt_payload'], jwt_payload)
        self.assertEqual(get_session_info(
            session_info['session']['handle']), session_data)

    def test_create_and_get_session_AT_expires_1_sec(self):
        new_settings = {
            "ACCESS_TOKEN_VALIDITY": 1
        }
        update_settings(new_settings)

        user_id = 'userId'
        jwt_payload = {'a': 'a'}
        session_data = {'b': 'b'}

        session = create_new_session(user_id, jwt_payload, session_data)
        validate(session, schema_create_new_session_ACT_enabled)

        session_info = get_session(
            session['access_token']['value'], session['anti_csrf_token'])
        validate(session_info, schema_new_session_get)

        sleep(1.5)
        try:
            get_session(session['access_token']['value'],
                        session['anti_csrf_token'])
            self.assertTrue(False)
        except SuperTokensTryRefreshTokenException:
            self.assertTrue(True)

    def test_create_and_get_session_AT_with_very_short_update_interval_for_signingkey(self):
        new_settings = {
            "ACCESS_TOKEN_SIGNING_KEY_UPDATE_INTERVAL": 0.0005
        }
        update_settings(new_settings)

        user_id = 'userId'
        jwt_payload = {'a': 'a'}
        session_data = {'b': 'b'}

        session = create_new_session(user_id, jwt_payload, session_data)
        validate(session, schema_create_new_session_ACT_enabled)

        session_info = get_session(
            session['access_token']['value'], session['anti_csrf_token'])
        validate(session_info, schema_new_session_get)

        sleep(2)
        try:
            get_session(session['access_token']['value'],
                        session['anti_csrf_token'])
            self.assertTrue(False)
        except SuperTokensTryRefreshTokenException:
            self.assertTrue(True)

    def test_altering_payload(self):
        user_id = 'userId'
        jwt_payload = {'a': 'a'}
        session_data = {'b': 'b'}

        session = create_new_session(user_id, jwt_payload, session_data)
        validate(session, schema_create_new_session_ACT_enabled)

        actual_splitted_token = session['access_token']['value'].split('.')
        get_session(session['access_token']['value'], session['anti_csrf_token'])
        jwt_payload['c'] = 'c'
        altered_payload = base64encode(dumps(jwt_payload))
        altered_token = actual_splitted_token[0] + '.' + \
            altered_payload + '.' + actual_splitted_token[2]
        try:
            get_session(altered_token, session['anti_csrf_token'])
            self.assertTrue(False)
        except SuperTokensTryRefreshTokenException:
            self.assertTrue(True)

    def test_refresh_session_ACT_enabled(self):
        new_settings = {
            "ACCESS_TOKEN_VALIDITY": 1
        }
        update_settings(new_settings)

        user_id = 'userId'
        jwt_payload = {'a': 'a'}
        session_data = {'b': 'b'}

        session = create_new_session(user_id, jwt_payload, session_data)
        validate(session, schema_create_new_session_ACT_enabled)

        sleep(1.5)
        try:
            get_session(session['access_token']['value'],
                        session['anti_csrf_token'])
            self.assertTrue(False)
        except SuperTokensTryRefreshTokenException:
            self.assertTrue(True)

        new_refreshed_session = refresh_session(
            session['refresh_token']['value'])
        validate(new_refreshed_session, schema_refresh_session_ACT_enabled)
        self.assertEqual(
            new_refreshed_session['session']['jwt_payload'], jwt_payload)
        self.assertEqual(get_session_info(
            new_refreshed_session['session']['handle']), session_data)

        session_info = get_session(
            new_refreshed_session['new_access_token']['value'], new_refreshed_session['new_anti_csrf_token'])
        validate(session_info, schema_updated_access_token_session_get)
        self.assertEqual(session_info['session']['jwt_payload'], jwt_payload)
        self.assertEqual(get_session_info(
            session_info['session']['handle']), session_data)
        self.assertNotEqual(
            session_info['new_access_token'], new_refreshed_session['new_access_token']['value'])

        new_access_token = session_info['new_access_token']
        session_info = get_session(
            session_info['new_access_token']['value'], new_refreshed_session['new_anti_csrf_token'])
        validate(session_info, schema_new_session_get)
        self.assertEqual(session_info['session']['jwt_payload'], jwt_payload)
        self.assertEqual(get_session_info(
            session_info['session']['handle']), session_data)

        sleep(1.5)
        try:
            get_session(
                new_access_token['value'], new_refreshed_session['new_anti_csrf_token'])
            self.assertTrue(False)
        except SuperTokensTryRefreshTokenException:
            self.assertTrue(True)

        new_refreshed_session = refresh_session(
            new_refreshed_session['new_refresh_token']['value'])
        validate(new_refreshed_session, schema_refresh_session_ACT_enabled)
        self.assertEqual(
            new_refreshed_session['session']['jwt_payload'], jwt_payload)
        self.assertEqual(get_session_info(
            new_refreshed_session['session']['handle']), session_data)

        session_info = get_session(
            new_refreshed_session['new_access_token']['value'], new_refreshed_session['new_anti_csrf_token'])
        validate(session_info, schema_updated_access_token_session_get)
        self.assertEqual(session_info['session']['jwt_payload'], jwt_payload)
        self.assertEqual(get_session_info(
            session_info['session']['handle']), session_data)
        self.assertNotEqual(
            session_info['new_access_token'], new_refreshed_session['new_access_token']['value'])

    def test_refresh_session_ACT_disabled(self):
        new_settings = {
            "ACCESS_TOKEN_VALIDITY": 1,
            "ANTI_CSRF_ENABLE": False
        }
        update_settings(new_settings)

        user_id = 'userId'
        jwt_payload = {'a': 'a'}
        session_data = {'b': 'b'}

        session = create_new_session(user_id, jwt_payload, session_data)
        validate(session, schema_create_new_session_ACT_disabled)

        sleep(1.5)
        try:
            get_session(session['access_token']['value'])
            self.assertTrue(False)
        except SuperTokensTryRefreshTokenException:
            self.assertTrue(True)

        new_refreshed_session = refresh_session(
            session['refresh_token']['value'])
        validate(new_refreshed_session, schema_refresh_session_ACT_disabled)
        self.assertEqual(
            new_refreshed_session['session']['jwt_payload'], jwt_payload)
        self.assertEqual(get_session_info(
            new_refreshed_session['session']['handle']), session_data)

        session_info = get_session(
            new_refreshed_session['new_access_token']['value'])
        validate(session_info, schema_updated_access_token_session_get)
        self.assertEqual(session_info['session']['jwt_payload'], jwt_payload)
        self.assertEqual(get_session_info(
            session_info['session']['handle']), session_data)
        self.assertNotEqual(
            session_info['new_access_token'], new_refreshed_session['new_access_token']['value'])

        new_access_token = session_info['new_access_token']
        session_info = get_session(session_info['new_access_token']['value'])
        validate(session_info, schema_new_session_get)
        self.assertEqual(session_info['session']['jwt_payload'], jwt_payload)
        self.assertEqual(get_session_info(
            session_info['session']['handle']), session_data)

        sleep(1.5)
        try:
            get_session(
                new_access_token['value'], new_refreshed_session['new_anti_csrf_token'])
            self.assertTrue(False)
        except SuperTokensTryRefreshTokenException:
            self.assertTrue(True)

        new_refreshed_session = refresh_session(
            new_refreshed_session['new_refresh_token']['value'])
        validate(new_refreshed_session, schema_refresh_session_ACT_disabled)
        self.assertEqual(
            new_refreshed_session['session']['jwt_payload'], jwt_payload)
        self.assertEqual(get_session_info(
            new_refreshed_session['session']['handle']), session_data)

        session_info = get_session(
            new_refreshed_session['new_access_token']['value'])
        validate(session_info, schema_updated_access_token_session_get)
        self.assertEqual(session_info['session']['jwt_payload'], jwt_payload)
        self.assertEqual(get_session_info(
            session_info['session']['handle']), session_data)
        self.assertNotEqual(
            session_info['new_access_token'], new_refreshed_session['new_access_token']['value'])

    def test_refresh_session_RT_expires_3_secs(self):
        new_settings = {
            "REFRESH_TOKEN_VALIDITY": 0.0008
        }
        update_settings(new_settings)

        user_id = 'userId'
        jwt_payload = {'a': 'a'}
        session_data = {'b': 'b'}

        session = create_new_session(user_id, jwt_payload, session_data)
        validate(session, schema_create_new_session_ACT_enabled)

        refreshed_session = refresh_session(session['refresh_token']['value'])
        validate(refreshed_session, schema_refresh_session_ACT_enabled)

        session_info = get_session(
            refreshed_session['new_access_token']['value'], refreshed_session['new_anti_csrf_token'])
        validate(session_info, schema_updated_access_token_session_get)

        sleep(4)
        try:
            refresh_session(refreshed_session['new_refresh_token']['value'])
            self.assertTrue(False)
        except SuperTokensUnauthorizedException:
            self.assertTrue(True)

        session = create_new_session(user_id, jwt_payload, session_data)
        validate(session, schema_create_new_session_ACT_enabled)

        refreshed_session = refresh_session(session['refresh_token']['value'])
        validate(refreshed_session, schema_refresh_session_ACT_enabled)

        session_info = get_session(
            refreshed_session['new_access_token']['value'], refreshed_session['new_anti_csrf_token'])
        validate(session_info, schema_updated_access_token_session_get)

        sleep(1)
        refreshed_session = refresh_session(
            refreshed_session['new_refresh_token']['value'])
        validate(refreshed_session, schema_refresh_session_ACT_enabled)

        sleep(1)
        refreshed_session = refresh_session(
            refreshed_session['new_refresh_token']['value'])
        validate(refreshed_session, schema_refresh_session_ACT_enabled)

    def test_revoke_all_user_sessions_without_blacklisting(self):
        user_id = 'userId'
        jwt_payload = {'a': 'a'}
        session_data = {'b': 'b'}

        session_1 = create_new_session(user_id, jwt_payload, session_data)
        validate(session_1, schema_create_new_session_ACT_enabled)
        session_2 = create_new_session(user_id, jwt_payload, session_data)
        validate(session_2, schema_create_new_session_ACT_enabled)
        session_3 = create_new_session(user_id, jwt_payload, session_data)
        validate(session_3, schema_create_new_session_ACT_enabled)

        self.assertEqual(RefreshTokenModel.objects.all().count(), 3)
        revoke_all_sessions_for_user(user_id)
        self.assertEqual(RefreshTokenModel.objects.all().count(), 0)

        session_info_1 = get_session(
            session_1['access_token']['value'], session_1['anti_csrf_token'])
        validate(session_info_1, schema_new_session_get)
        session_info_2 = get_session(
            session_2['access_token']['value'], session_2['anti_csrf_token'])
        validate(session_info_2, schema_new_session_get)
        session_info_3 = get_session(
            session_3['access_token']['value'], session_3['anti_csrf_token'])
        validate(session_info_3, schema_new_session_get)

    def test_revoke_all_user_sessions_with_blacklisting(self):
        new_settings = {
            "ACCESS_TOKEN_ENABLE_BLACKLISTING": True
        }
        update_settings(new_settings)
        user_id = 'userId'
        jwt_payload = {'a': 'a'}
        session_data = {'b': 'b'}

        session_1 = create_new_session(user_id, jwt_payload, session_data)
        validate(session_1, schema_create_new_session_ACT_enabled)
        session_2 = create_new_session(user_id, jwt_payload, session_data)
        validate(session_2, schema_create_new_session_ACT_enabled)
        session_3 = create_new_session(user_id, jwt_payload, session_data)
        validate(session_3, schema_create_new_session_ACT_enabled)

        self.assertEqual(RefreshTokenModel.objects.all().count(), 3)
        revoke_all_sessions_for_user(user_id)
        self.assertEqual(RefreshTokenModel.objects.all().count(), 0)

        try:
            get_session(session_1['access_token']['value'],
                        session_1['anti_csrf_token'])
            self.assertTrue(False)
        except Exception:
            self.assertTrue(True)

        try:
            get_session(session_2['access_token']['value'],
                        session_2['anti_csrf_token'])
            self.assertTrue(False)
        except Exception:
            self.assertTrue(True)

        try:
            get_session(session_3['access_token']['value'],
                        session_3['anti_csrf_token'])
            self.assertTrue(False)
        except Exception:
            self.assertTrue(True)

    def test_update_session_info(self):
        user_id = 'userId'
        jwt_payload = {'a': 'a'}
        session_data = {'b': 'b'}

        session = create_new_session(user_id, jwt_payload, session_data)
        validate(session, schema_create_new_session_ACT_enabled)

        session_data_db = get_session_info(session['session']['handle'])
        self.assertEqual(session_data_db, session_data)

        new_session_info = 44
        update_session_info(session['session']['handle'], new_session_info)
        session_data_db = get_session_info(session['session']['handle'])
        self.assertEqual(session_data_db, new_session_info)

    def test_revoke_session_without_blacklisting(self):
        user_id = 'userId'
        jwt_payload = {'a': 'a'}
        session_data = {'b': 'b'}

        session_1 = create_new_session(user_id, jwt_payload, session_data)
        validate(session_1, schema_create_new_session_ACT_enabled)
        session_2 = create_new_session(user_id, jwt_payload, session_data)
        validate(session_2, schema_create_new_session_ACT_enabled)

        self.assertEqual(RefreshTokenModel.objects.all().count(), 2)
        self.assertTrue(revoke_session(session_1['session']['handle']))
        self.assertEqual(RefreshTokenModel.objects.all().count(), 1)

        try:
            refresh_session(session_1['refresh_token']['value'])
            self.assertTrue(False)
        except Exception:
            self.assertTrue(True)

        refresh_session(session_2['refresh_token']['value'])

        session_info_1 = get_session(
            session_1['access_token']['value'], session_1['anti_csrf_token'])
        validate(session_info_1, schema_new_session_get)

    def test_revoke_session_with_blacklisting(self):
        new_settings = {
            "ACCESS_TOKEN_ENABLE_BLACKLISTING": True
        }
        update_settings(new_settings)
        user_id = 'userId'
        jwt_payload = {'a': 'a'}
        session_data = {'b': 'b'}

        session_1 = create_new_session(user_id, jwt_payload, session_data)
        validate(session_1, schema_create_new_session_ACT_enabled)
        session_2 = create_new_session(user_id, jwt_payload, session_data)
        validate(session_2, schema_create_new_session_ACT_enabled)

        self.assertEqual(RefreshTokenModel.objects.all().count(), 2)
        self.assertTrue(revoke_session(session_1['session']['handle']))
        self.assertEqual(RefreshTokenModel.objects.all().count(), 1)

        try:
            refresh_session(session_1['refresh_token']['value'])
            self.assertTrue(False)
        except Exception:
            self.assertTrue(True)
        try:
            get_session(session_1['access_token']['value'],
                        session_1['anti_csrf_token'])
            self.assertTrue(False)
        except Exception:
            self.assertTrue(True)

        session_info_2 = get_session(
            session_2['access_token']['value'], session_2['anti_csrf_token'])
        validate(session_info_2, schema_new_session_get)
        refresh_session(session_2['refresh_token']['value'])

    def test_user_id_numeric(self):
        new_settings = {
            "ACCESS_TOKEN_VALIDITY": 1
        }
        update_settings(new_settings)

        user_id = 1
        jwt_payload = {'a': 'a'}
        session_data = {'b': 'b'}

        session = create_new_session(user_id, jwt_payload, session_data)
        validate(session, schema_create_new_session_ACT_enabled)
        self.assertEqual(session['session']['user_id'], user_id)

        session_info = get_session(
            session['access_token']['value'], session['anti_csrf_token'])
        validate(session_info, schema_new_session_get)
        self.assertEqual(session_info['session']['user_id'], user_id)

        sleep(1.5)
        try:
            get_session(session['access_token']['value'],
                        session['anti_csrf_token'])
            self.assertTrue(False)
        except Exception:
            self.assertTrue(True)

        refreshed_session = refresh_session(session['refresh_token']['value'])
        validate(refreshed_session, schema_refresh_session_ACT_enabled)
        self.assertEqual(refreshed_session['session']['user_id'], user_id)

    def test_user_id_number_as_string(self):
        new_settings = {
            "ACCESS_TOKEN_VALIDITY": 1
        }
        update_settings(new_settings)

        user_id = "1"
        jwt_payload = {'a': 'a'}
        session_data = {'b': 'b'}

        session = create_new_session(user_id, jwt_payload, session_data)
        validate(session, schema_create_new_session_ACT_enabled)
        self.assertEqual(session['session']['user_id'], user_id)

        session_info = get_session(
            session['access_token']['value'], session['anti_csrf_token'])
        validate(session_info, schema_new_session_get)
        self.assertEqual(session_info['session']['user_id'], user_id)

        sleep(1.5)
        try:
            get_session(session['access_token']['value'],
                        session['anti_csrf_token'])
            self.assertTrue(False)
        except Exception:
            self.assertTrue(True)

        refreshed_session = refresh_session(session['refresh_token']['value'])
        validate(refreshed_session, schema_refresh_session_ACT_enabled)
        self.assertEqual(refreshed_session['session']['user_id'], user_id)

    def test_user_id_stringified_json_type_one(self):
        new_settings = {
            "ACCESS_TOKEN_VALIDITY": 1
        }
        update_settings(new_settings)

        user_id = dumps({'a': 'a'})
        jwt_payload = {'a': 'a'}
        session_data = {'b': 'b'}

        session = create_new_session(user_id, jwt_payload, session_data)
        validate(session, schema_create_new_session_ACT_enabled)
        self.assertEqual(session['session']['user_id'], user_id)

        session_info = get_session(
            session['access_token']['value'], session['anti_csrf_token'])
        validate(session_info, schema_new_session_get)
        self.assertEqual(session_info['session']['user_id'], user_id)

        sleep(1.5)
        try:
            get_session(session['access_token']['value'],
                        session['anti_csrf_token'])
            self.assertTrue(False)
        except Exception:
            self.assertTrue(True)

        refreshed_session = refresh_session(session['refresh_token']['value'])
        validate(refreshed_session, schema_refresh_session_ACT_enabled)
        self.assertEqual(refreshed_session['session']['user_id'], user_id)

    def test_user_id_stringified_json_type_multi(self):
        new_settings = {
            "ACCESS_TOKEN_VALIDITY": 1
        }
        update_settings(new_settings)

        user_id = dumps({'a': 'a', 'i': 'i'})
        jwt_payload = {'a': 'a'}
        session_data = {'b': 'b'}

        session = create_new_session(user_id, jwt_payload, session_data)
        validate(session, schema_create_new_session_ACT_enabled)
        self.assertEqual(session['session']['user_id'], user_id)

        session_info = get_session(
            session['access_token']['value'], session['anti_csrf_token'])
        validate(session_info, schema_new_session_get)
        self.assertEqual(session_info['session']['user_id'], user_id)

        sleep(1.5)
        try:
            get_session(session['access_token']['value'],
                        session['anti_csrf_token'])
            self.assertTrue(False)
        except Exception:
            self.assertTrue(True)

        refreshed_session = refresh_session(session['refresh_token']['value'])
        validate(refreshed_session, schema_refresh_session_ACT_enabled)
        self.assertEqual(refreshed_session['session']['user_id'], user_id)

    def test_user_id_stringified_invalid_json(self):
        user_id = dumps({'i': 'a'})
        jwt_payload = {'a': 'a'}
        session_data = {'b': 'b'}

        try:
            create_new_session(user_id, jwt_payload, session_data)
            self.assertTrue(False)
        except Exception:
            self.assertTrue(True)

    def test_token_theft_s1_r1_s2_r1(self):
        user_id = 'userId'
        jwt_payload = {'a': 'a'}
        session_data = {'b': 'b'}

        session = create_new_session(user_id, jwt_payload, session_data)
        validate(session, schema_create_new_session_ACT_enabled)

        refreshed_session = refresh_session(session['refresh_token']['value'])
        validate(refreshed_session, schema_refresh_session_ACT_enabled)

        session_info = get_session(
            refreshed_session['new_access_token']['value'], refreshed_session['new_anti_csrf_token'])
        validate(session_info, schema_updated_access_token_session_get)

        try:
            refresh_session(session['refresh_token']['value'])
            self.assertTrue(False)
        except SuperTokensTokenTheftException as e:
            self.assertEqual(user_id, e.get_user_id())
            self.assertEqual(session['session']
                             ['handle'], e.get_session_handle())

    def test_token_theft_s1_r1_r2_r1(self):
        user_id = 'userId'
        jwt_payload = {'a': 'a'}
        session_data = {'b': 'b'}

        session = create_new_session(user_id, jwt_payload, session_data)
        validate(session, schema_create_new_session_ACT_enabled)

        refreshed_session = refresh_session(session['refresh_token']['value'])
        validate(refreshed_session, schema_refresh_session_ACT_enabled)

        refreshed_session = refresh_session(
            refreshed_session['new_refresh_token']['value'])
        validate(refreshed_session, schema_refresh_session_ACT_enabled)

        try:
            refresh_session(session['refresh_token']['value'])
            self.assertTrue(False)
        except SuperTokensTokenTheftException as e:
            self.assertEqual(user_id, e.get_user_id())
            self.assertEqual(session['session']
                             ['handle'], e.get_session_handle())

    def test_remove_expired_sessions(self):
        new_settings = {
            "REFRESH_TOKEN_VALIDITY": 0.0005
        }
        update_settings(new_settings)

        user_id = 'userId'
        jwt_payload = {'a': 'a'}
        session_data = {'b': 'b'}

        create_new_session(user_id, jwt_payload, session_data)
        create_new_session(user_id, jwt_payload, session_data)
        create_new_session(user_id, jwt_payload, session_data)
        self.assertEqual(RefreshTokenModel.objects.all().count(), 3)

        sleep(2)

        create_new_session(user_id, jwt_payload, session_data)
        remove_expired_tokens()
        self.assertEqual(RefreshTokenModel.objects.all().count(), 1)
