from django.test import TestCase, RequestFactory
from django.http import HttpResponse
from .utils import set_default_settings, update_settings
from supertokens_jwt_ref.refresh_token_signing_key import RefreshTokenSigningKey
from supertokens_jwt_ref.access_token_singingkey import AccessTokenSigningKey
from supertokens_jwt_ref import supertokens
from time import sleep
from supertokens_jwt_ref.exceptions import (
    SuperTokensTokenTheftException,
    SuperTokensUnauthorizedException,
    SuperTokensTryRefreshTokenException
)


class SupertokensTest(TestCase):

    def setUp(self):
        set_default_settings()
        AccessTokenSigningKey.reset_instance()
        RefreshTokenSigningKey.reset_instance()
        self.factory = RequestFactory()

    def test_create_get_refresh_session_with_token_theft_ACT_enabled_and_cookie_path(self):
        access_token_path = 'testing/'
        refresh_token_path = 'refresh/'

        new_settings = {
            "ACCESS_TOKEN_SIGNING_KEY_UPDATE_INTERVAL": 0.0005,
            "ACCESS_TOKEN_PATH": access_token_path
        }
        update_settings(new_settings)

        user_id = 'userId'
        jwt_payload = {'a': 'a'}
        session_data = {'b': 'b'}

        response = HttpResponse()

        supertokens.create_new_session(
            response, user_id, jwt_payload, session_data)

        access_token_cookie = response.cookies.get("sAccessToken")
        refresh_token_cookie = response.cookies.get("sRefreshToken")
        id_refresh_token_cookie = response.cookies.get(
            "sIdRefreshToken")
        self.assertTrue(response.has_header("ANTI-CSRF"))
        anti_csrf_token = response.get("ANTI-CSRF")

        self.assertIsNotNone(access_token_cookie)
        self.assertIsNotNone(refresh_token_cookie)
        self.assertIsNotNone(id_refresh_token_cookie)
        self.assertEqual(access_token_path, access_token_cookie['path'])
        self.assertEqual(refresh_token_path, refresh_token_cookie['path'])
        self.assertEqual(access_token_path, id_refresh_token_cookie['path'])
        access_token_cookie = access_token_cookie.value
        refresh_token_cookie = refresh_token_cookie.value
        id_refresh_token_cookie = id_refresh_token_cookie.value

        request = request = self.factory.get(
            '/', **{'HTTP_ANTI_CSRF': anti_csrf_token})
        request.COOKIES["sAccessToken"] = access_token_cookie
        request.COOKIES["sIdRefreshToken"] = id_refresh_token_cookie
        response = HttpResponse()

        session = supertokens.get_session(request, response, True)
        self.assertEqual(session.get_user_id(), user_id)

        sleep(2)
        request = request = self.factory.get(
            '/', **{'HTTP_ANTI_CSRF': anti_csrf_token})
        request.COOKIES["sAccessToken"] = access_token_cookie
        request.COOKIES["sIdRefreshToken"] = id_refresh_token_cookie
        response = HttpResponse()

        try:
            supertokens.get_session(request, response, True)
            self.assertTrue(False)
        except SuperTokensTryRefreshTokenException:
            self.assertTrue(True)

        request = request = self.factory.get('/')
        request.COOKIES["sAccessToken"] = access_token_cookie
        request.COOKIES["sIdRefreshToken"] = id_refresh_token_cookie
        request.COOKIES["sRefreshToken"] = refresh_token_cookie
        response = HttpResponse()
        supertokens.refresh_session(request, response)

        old_access_token_cookie = access_token_cookie
        old_refresh_token_cookie = refresh_token_cookie
        old_id_refresh_token_cookie = id_refresh_token_cookie
        access_token_cookie = response.cookies.get("sAccessToken")
        refresh_token_cookie = response.cookies.get("sRefreshToken")
        id_refresh_token_cookie = response.cookies.get(
            "sIdRefreshToken")
        self.assertTrue(response.has_header("ANTI-CSRF"))
        anti_csrf_token = response.get("ANTI-CSRF")

        self.assertIsNotNone(access_token_cookie)
        self.assertIsNotNone(refresh_token_cookie)
        self.assertIsNotNone(id_refresh_token_cookie)
        self.assertEqual(access_token_path, access_token_cookie['path'])
        self.assertEqual(refresh_token_path, refresh_token_cookie['path'])
        self.assertEqual(access_token_path, id_refresh_token_cookie['path'])
        access_token_cookie = access_token_cookie.value
        refresh_token_cookie = refresh_token_cookie.value
        id_refresh_token_cookie = id_refresh_token_cookie.value
        self.assertNotEqual(access_token_cookie, old_access_token_cookie)
        self.assertNotEqual(refresh_token_cookie, old_refresh_token_cookie)
        self.assertNotEqual(id_refresh_token_cookie,
                            old_id_refresh_token_cookie)

        request = request = self.factory.get(
            '/', **{'HTTP_ANTI_CSRF': anti_csrf_token})
        request.COOKIES["sAccessToken"] = access_token_cookie
        request.COOKIES["sIdRefreshToken"] = id_refresh_token_cookie
        response = HttpResponse()

        supertokens.get_session(request, response, True)

        request = request = self.factory.get('/')
        request.COOKIES["sAccessToken"] = access_token_cookie
        request.COOKIES["sIdRefreshToken"] = id_refresh_token_cookie
        response = HttpResponse()

        try:
            supertokens.get_session(request, response, True)
            self.assertTrue(False)
        except SuperTokensTryRefreshTokenException:
            self.assertTrue(True)

        request = request = self.factory.get('/')
        request.COOKIES["sAccessToken"] = old_access_token_cookie
        request.COOKIES["sIdRefreshToken"] = old_id_refresh_token_cookie
        request.COOKIES["sRefreshToken"] = old_refresh_token_cookie
        response = HttpResponse()
        try:
            supertokens.refresh_session(request, response)
            self.assertTrue(False)
        except SuperTokensTokenTheftException:
            self.assertTrue(True)

        access_token_cookie = response.cookies.get("sAccessToken")
        refresh_token_cookie = response.cookies.get("sRefreshToken")
        id_refresh_token_cookie = response.cookies.get(
            "sIdRefreshToken")

        self.assertIsNotNone(access_token_cookie)
        self.assertIsNotNone(refresh_token_cookie)
        self.assertIsNotNone(id_refresh_token_cookie)
        self.assertEqual(access_token_path, access_token_cookie['path'])
        self.assertEqual(refresh_token_path, refresh_token_cookie['path'])
        self.assertEqual(access_token_path, id_refresh_token_cookie['path'])
        access_token_cookie = access_token_cookie.value
        refresh_token_cookie = refresh_token_cookie.value
        id_refresh_token_cookie = id_refresh_token_cookie.value
        self.assertEqual(access_token_cookie, '')
        self.assertEqual(refresh_token_cookie, '')
        self.assertEqual(id_refresh_token_cookie, '')

    def test_create_get_refresh_session_with_token_theft_ACT_disabled_and_cookie_path(self):
        access_token_path = 'testing/'
        refresh_token_path = 'refresh/'

        new_settings = {
            "ACCESS_TOKEN_SIGNING_KEY_UPDATE_INTERVAL": 0.0005,
            "ACCESS_TOKEN_PATH": access_token_path,
            "ANTI_CSRF_ENABLE": False
        }
        update_settings(new_settings)

        user_id = 'userId'
        jwt_payload = {'a': 'a'}
        session_data = {'b': 'b'}

        response = HttpResponse()

        supertokens.create_new_session(
            response, user_id, jwt_payload, session_data)

        access_token_cookie = response.cookies.get("sAccessToken")
        refresh_token_cookie = response.cookies.get("sRefreshToken")
        id_refresh_token_cookie = response.cookies.get(
            "sIdRefreshToken")
        self.assertTrue(not response.has_header("ANTI-CSRF"))

        self.assertIsNotNone(access_token_cookie)
        self.assertIsNotNone(refresh_token_cookie)
        self.assertIsNotNone(id_refresh_token_cookie)
        self.assertEqual(access_token_path, access_token_cookie['path'])
        self.assertEqual(refresh_token_path, refresh_token_cookie['path'])
        self.assertEqual(access_token_path, id_refresh_token_cookie['path'])
        access_token_cookie = access_token_cookie.value
        refresh_token_cookie = refresh_token_cookie.value
        id_refresh_token_cookie = id_refresh_token_cookie.value

        request = request = self.factory.get('/')
        request.COOKIES["sAccessToken"] = access_token_cookie
        request.COOKIES["sIdRefreshToken"] = id_refresh_token_cookie
        response = HttpResponse()

        session = supertokens.get_session(request, response, False)
        self.assertEqual(session.get_user_id(), user_id)

        sleep(2)
        request = request = self.factory.get('/')
        request.COOKIES["sAccessToken"] = access_token_cookie
        request.COOKIES["sIdRefreshToken"] = id_refresh_token_cookie
        response = HttpResponse()

        try:
            supertokens.get_session(request, response, False)
            self.assertTrue(False)
        except SuperTokensTryRefreshTokenException:
            self.assertTrue(True)

        request = request = self.factory.get('/')
        request.COOKIES["sAccessToken"] = access_token_cookie
        request.COOKIES["sIdRefreshToken"] = id_refresh_token_cookie
        request.COOKIES["sRefreshToken"] = refresh_token_cookie
        response = HttpResponse()
        supertokens.refresh_session(request, response)

        old_access_token_cookie = access_token_cookie
        old_refresh_token_cookie = refresh_token_cookie
        old_id_refresh_token_cookie = id_refresh_token_cookie
        access_token_cookie = response.cookies.get("sAccessToken")
        refresh_token_cookie = response.cookies.get("sRefreshToken")
        id_refresh_token_cookie = response.cookies.get(
            "sIdRefreshToken")
        self.assertTrue(not response.has_header("ANTI-CSRF"))

        self.assertIsNotNone(access_token_cookie)
        self.assertIsNotNone(refresh_token_cookie)
        self.assertIsNotNone(id_refresh_token_cookie)
        self.assertEqual(access_token_path, access_token_cookie['path'])
        self.assertEqual(refresh_token_path, refresh_token_cookie['path'])
        self.assertEqual(access_token_path, id_refresh_token_cookie['path'])
        access_token_cookie = access_token_cookie.value
        refresh_token_cookie = refresh_token_cookie.value
        id_refresh_token_cookie = id_refresh_token_cookie.value
        self.assertNotEqual(access_token_cookie, old_access_token_cookie)
        self.assertNotEqual(refresh_token_cookie, old_refresh_token_cookie)
        self.assertNotEqual(id_refresh_token_cookie,
                            old_id_refresh_token_cookie)

        request = request = self.factory.get('/')
        request.COOKIES["sAccessToken"] = access_token_cookie
        request.COOKIES["sIdRefreshToken"] = id_refresh_token_cookie
        response = HttpResponse()

        supertokens.get_session(request, response, True)

        request = request = self.factory.get('/')
        request.COOKIES["sAccessToken"] = old_access_token_cookie
        request.COOKIES["sIdRefreshToken"] = old_id_refresh_token_cookie
        request.COOKIES["sRefreshToken"] = old_refresh_token_cookie
        response = HttpResponse()
        try:
            supertokens.refresh_session(request, response)
            self.assertTrue(False)
        except SuperTokensTokenTheftException:
            self.assertTrue(True)

        access_token_cookie = response.cookies.get("sAccessToken")
        refresh_token_cookie = response.cookies.get("sRefreshToken")
        id_refresh_token_cookie = response.cookies.get(
            "sIdRefreshToken")

        self.assertIsNotNone(access_token_cookie)
        self.assertIsNotNone(refresh_token_cookie)
        self.assertIsNotNone(id_refresh_token_cookie)
        self.assertEqual(access_token_path, access_token_cookie['path'])
        self.assertEqual(refresh_token_path, refresh_token_cookie['path'])
        self.assertEqual(access_token_path, id_refresh_token_cookie['path'])
        access_token_cookie = access_token_cookie.value
        refresh_token_cookie = refresh_token_cookie.value
        id_refresh_token_cookie = id_refresh_token_cookie.value
        self.assertEqual(access_token_cookie, '')
        self.assertEqual(refresh_token_cookie, '')
        self.assertEqual(id_refresh_token_cookie, '')

    def test_revoke_session_without_blacklisting(self):
        user_id = 'userId'
        jwt_payload = {'a': 'a'}
        session_data = {'b': 'b'}

        response = HttpResponse()

        supertokens.create_new_session(
            response, user_id, jwt_payload, session_data)

        access_token_cookie = response.cookies.get("sAccessToken")
        refresh_token_cookie = response.cookies.get("sRefreshToken")
        id_refresh_token_cookie = response.cookies.get(
            "sIdRefreshToken")
        self.assertTrue(response.has_header("ANTI-CSRF"))
        anti_csrf_token = response.get("ANTI-CSRF")

        self.assertIsNotNone(access_token_cookie)
        self.assertIsNotNone(refresh_token_cookie)
        self.assertIsNotNone(id_refresh_token_cookie)
        access_token_cookie = access_token_cookie.value
        refresh_token_cookie = refresh_token_cookie.value
        id_refresh_token_cookie = id_refresh_token_cookie.value

        request = request = self.factory.get(
            '/', **{'HTTP_' + "ANTI_CSRF": anti_csrf_token})
        request.COOKIES["sAccessToken"] = access_token_cookie
        request.COOKIES["sIdRefreshToken"] = id_refresh_token_cookie
        response = HttpResponse()

        session = supertokens.get_session(request, response, True)
        self.assertEqual(session.get_user_id(), user_id)

        session.revoke_session()

        request = request = self.factory.get(
            '/', **{'HTTP_' + "ANTI_CSRF": anti_csrf_token})
        request.COOKIES["sAccessToken"] = access_token_cookie
        request.COOKIES["sIdRefreshToken"] = id_refresh_token_cookie
        response = HttpResponse()

        request = request = self.factory.get('/')
        request.COOKIES["sAccessToken"] = access_token_cookie
        request.COOKIES["sIdRefreshToken"] = id_refresh_token_cookie
        request.COOKIES["sRefreshToken"] = refresh_token_cookie
        response = HttpResponse()
        try:
            supertokens.refresh_session(request, response)
            self.assertTrue(False)
        except SuperTokensUnauthorizedException:
            self.assertTrue(True)

        request = request = self.factory.get(
            '/', **{'HTTP_' + "ANTI_CSRF": anti_csrf_token})
        request.COOKIES["sAccessToken"] = access_token_cookie
        request.COOKIES["sIdRefreshToken"] = id_refresh_token_cookie
        response = HttpResponse()
        session = supertokens.get_session(request, response, True)
        self.assertEqual(session.get_user_id(), user_id)

    def test_revoke_session_with_blacklisting(self):
        new_settings = {
            "ACCESS_TOKEN_ENABLE_BLACKLISTING": True
        }
        update_settings(new_settings)
        user_id = 'userId'
        jwt_payload = {'a': 'a'}
        session_data = {'b': 'b'}

        response = HttpResponse()

        supertokens.create_new_session(
            response, user_id, jwt_payload, session_data)

        access_token_cookie = response.cookies.get("sAccessToken")
        refresh_token_cookie = response.cookies.get("sRefreshToken")
        id_refresh_token_cookie = response.cookies.get(
            "sIdRefreshToken")
        self.assertTrue(response.has_header("ANTI-CSRF"))
        anti_csrf_token = response.get("ANTI-CSRF")

        self.assertIsNotNone(access_token_cookie)
        self.assertIsNotNone(refresh_token_cookie)
        self.assertIsNotNone(id_refresh_token_cookie)
        access_token_cookie = access_token_cookie.value
        refresh_token_cookie = refresh_token_cookie.value
        id_refresh_token_cookie = id_refresh_token_cookie.value

        request = request = self.factory.get(
            '/', **{'HTTP_' + "ANTI_CSRF": anti_csrf_token})
        request.COOKIES["sAccessToken"] = access_token_cookie
        request.COOKIES["sIdRefreshToken"] = id_refresh_token_cookie
        response = HttpResponse()

        session = supertokens.get_session(request, response, True)
        self.assertEqual(session.get_user_id(), user_id)

        session.revoke_session()

        request = request = self.factory.get(
            '/', **{'HTTP_' + "ANTI_CSRF": anti_csrf_token})
        request.COOKIES["sAccessToken"] = access_token_cookie
        request.COOKIES["sIdRefreshToken"] = id_refresh_token_cookie
        response = HttpResponse()

        request = request = self.factory.get('/')
        request.COOKIES["sAccessToken"] = access_token_cookie
        request.COOKIES["sIdRefreshToken"] = id_refresh_token_cookie
        request.COOKIES["sRefreshToken"] = refresh_token_cookie
        response = HttpResponse()
        try:
            supertokens.refresh_session(request, response)
            self.assertTrue(False)
        except SuperTokensUnauthorizedException:
            self.assertTrue(True)

        request = request = self.factory.get(
            '/', **{'HTTP_' + "ANTI_CSRF": anti_csrf_token})
        request.COOKIES["sAccessToken"] = access_token_cookie
        request.COOKIES["sIdRefreshToken"] = id_refresh_token_cookie
        response = HttpResponse()
        try:
            supertokens.get_session(request, response, True)
            self.assertTrue(False)
        except SuperTokensUnauthorizedException:
            self.assertTrue(True)

    def test_refresh_token_expired(self):
        user_id = 'userId'
        jwt_payload = {'a': 'a'}
        session_data = {'b': 'b'}

        response = HttpResponse()

        supertokens.create_new_session(
            response, user_id, jwt_payload, session_data)

        access_token_cookie = response.cookies.get("sAccessToken")
        refresh_token_cookie = response.cookies.get("sRefreshToken")
        id_refresh_token_cookie = response.cookies.get(
            "sIdRefreshToken")
        self.assertTrue(response.has_header("ANTI-CSRF"))
        anti_csrf_token = response.get("ANTI-CSRF")

        self.assertIsNotNone(access_token_cookie)
        self.assertIsNotNone(refresh_token_cookie)
        self.assertIsNotNone(id_refresh_token_cookie)
        access_token_cookie = access_token_cookie.value
        refresh_token_cookie = refresh_token_cookie.value
        id_refresh_token_cookie = id_refresh_token_cookie.value

        request = request = self.factory.get(
            '/', **{'HTTP_' + "ANTI_CSRF": anti_csrf_token})
        request.COOKIES["sAccessToken"] = access_token_cookie
        request.COOKIES["sIdRefreshToken"] = id_refresh_token_cookie
        response = HttpResponse()

        session = supertokens.get_session(request, response, True)
        self.assertEqual(session.get_user_id(), user_id)

        RefreshTokenSigningKey.reset_instance()

        request = request = self.factory.get('/')
        request.COOKIES["sAccessToken"] = access_token_cookie
        request.COOKIES["sIdRefreshToken"] = id_refresh_token_cookie
        request.COOKIES["sRefreshToken"] = refresh_token_cookie
        response = HttpResponse()
        try:
            supertokens.refresh_session(request, response)
            self.assertTrue(False)
        except SuperTokensUnauthorizedException:
            self.assertTrue(True)

        access_token_cookie = response.cookies.get("sAccessToken")
        refresh_token_cookie = response.cookies.get("sRefreshToken")
        id_refresh_token_cookie = response.cookies.get(
            "sIdRefreshToken")

        self.assertIsNotNone(access_token_cookie)
        self.assertIsNotNone(refresh_token_cookie)
        self.assertIsNotNone(id_refresh_token_cookie)
        access_token_cookie = access_token_cookie.value
        refresh_token_cookie = refresh_token_cookie.value
        id_refresh_token_cookie = id_refresh_token_cookie.value
        self.assertEqual(access_token_cookie, '')
        self.assertEqual(refresh_token_cookie, '')
        self.assertEqual(id_refresh_token_cookie, '')

    def test_revoke_all_sessions_without_blacklisting(self):
        user_id = 'userId'
        jwt_payload = {'a': 'a'}
        session_data = {'b': 'b'}

        response = HttpResponse()
        supertokens.create_new_session(
            response, user_id, jwt_payload, session_data)

        access_token_cookie = response.cookies.get("sAccessToken")
        refresh_token_cookie = response.cookies.get("sRefreshToken")
        id_refresh_token_cookie = response.cookies.get(
            "sIdRefreshToken")
        self.assertTrue(response.has_header("ANTI-CSRF"))
        anti_csrf_token_1 = response.get("ANTI-CSRF")

        self.assertIsNotNone(access_token_cookie)
        self.assertIsNotNone(refresh_token_cookie)
        self.assertIsNotNone(id_refresh_token_cookie)
        access_token_cookie_1 = access_token_cookie.value
        refresh_token_cookie_1 = refresh_token_cookie.value
        id_refresh_token_cookie_1 = id_refresh_token_cookie.value

        response = HttpResponse()
        supertokens.create_new_session(
            response, user_id, jwt_payload, session_data)

        access_token_cookie = response.cookies.get("sAccessToken")
        refresh_token_cookie = response.cookies.get("sRefreshToken")
        id_refresh_token_cookie = response.cookies.get(
            "sIdRefreshToken")
        self.assertTrue(response.has_header("ANTI-CSRF"))
        anti_csrf_token_2 = response.get("ANTI-CSRF")

        self.assertIsNotNone(access_token_cookie)
        self.assertIsNotNone(refresh_token_cookie)
        self.assertIsNotNone(id_refresh_token_cookie)
        access_token_cookie_2 = access_token_cookie.value
        refresh_token_cookie_2 = refresh_token_cookie.value
        id_refresh_token_cookie_2 = id_refresh_token_cookie.value

        response = HttpResponse()
        supertokens.create_new_session(
            response, user_id, jwt_payload, session_data)

        access_token_cookie = response.cookies.get("sAccessToken")
        refresh_token_cookie = response.cookies.get("sRefreshToken")
        id_refresh_token_cookie = response.cookies.get(
            "sIdRefreshToken")
        self.assertTrue(response.has_header("ANTI-CSRF"))
        anti_csrf_token_3 = response.get("ANTI-CSRF")

        self.assertIsNotNone(access_token_cookie)
        self.assertIsNotNone(refresh_token_cookie)
        self.assertIsNotNone(id_refresh_token_cookie)
        access_token_cookie_3 = access_token_cookie.value
        refresh_token_cookie_3 = refresh_token_cookie.value
        id_refresh_token_cookie_3 = id_refresh_token_cookie.value

        supertokens.revoke_all_sessions_for_user(user_id)

        request = request = self.factory.get('/')
        request.COOKIES["sAccessToken"] = access_token_cookie_1
        request.COOKIES["sIdRefreshToken"] = id_refresh_token_cookie_1
        request.COOKIES["sRefreshToken"] = refresh_token_cookie_1
        response = HttpResponse()
        try:
            supertokens.refresh_session(request, response)
            self.assertTrue(False)
        except SuperTokensUnauthorizedException:
            self.assertTrue(True)

        request = request = self.factory.get(
            '/', **{'HTTP_' + "ANTI_CSRF": anti_csrf_token_1})
        request.COOKIES["sAccessToken"] = access_token_cookie_1
        request.COOKIES["sIdRefreshToken"] = id_refresh_token_cookie_1
        response = HttpResponse()
        session = supertokens.get_session(request, response, True)
        self.assertEqual(session.get_user_id(), user_id)

        request = request = self.factory.get('/')
        request.COOKIES["sAccessToken"] = access_token_cookie_2
        request.COOKIES["sIdRefreshToken"] = id_refresh_token_cookie_2
        request.COOKIES["sRefreshToken"] = refresh_token_cookie_2
        response = HttpResponse()
        try:
            supertokens.refresh_session(request, response)
            self.assertTrue(False)
        except SuperTokensUnauthorizedException:
            self.assertTrue(True)

        request = request = self.factory.get(
            '/', **{'HTTP_' + "ANTI_CSRF": anti_csrf_token_2})
        request.COOKIES["sAccessToken"] = access_token_cookie_2
        request.COOKIES["sIdRefreshToken"] = id_refresh_token_cookie_2
        response = HttpResponse()
        session = supertokens.get_session(request, response, True)
        self.assertEqual(session.get_user_id(), user_id)

        request = request = self.factory.get('/')
        request.COOKIES["sAccessToken"] = access_token_cookie_3
        request.COOKIES["sIdRefreshToken"] = id_refresh_token_cookie_3
        request.COOKIES["sRefreshToken"] = refresh_token_cookie_3
        response = HttpResponse()
        try:
            supertokens.refresh_session(request, response)
            self.assertTrue(False)
        except SuperTokensUnauthorizedException:
            self.assertTrue(True)

        request = request = self.factory.get(
            '/', **{'HTTP_' + "ANTI_CSRF": anti_csrf_token_3})
        request.COOKIES["sAccessToken"] = access_token_cookie_3
        request.COOKIES["sIdRefreshToken"] = id_refresh_token_cookie_3
        response = HttpResponse()
        session = supertokens.get_session(request, response, True)
        self.assertEqual(session.get_user_id(), user_id)

    def test_revoke_all_sessions_with_blacklisting(self):
        new_settings = {
            "ACCESS_TOKEN_ENABLE_BLACKLISTING": True
        }
        update_settings(new_settings)
        user_id = 'userId'
        jwt_payload = {'a': 'a'}
        session_data = {'b': 'b'}

        response = HttpResponse()
        supertokens.create_new_session(
            response, user_id, jwt_payload, session_data)

        access_token_cookie = response.cookies.get("sAccessToken")
        refresh_token_cookie = response.cookies.get("sRefreshToken")
        id_refresh_token_cookie = response.cookies.get(
            "sIdRefreshToken")
        self.assertTrue(response.has_header("ANTI-CSRF"))
        anti_csrf_token_1 = response.get("ANTI-CSRF")

        self.assertIsNotNone(access_token_cookie)
        self.assertIsNotNone(refresh_token_cookie)
        self.assertIsNotNone(id_refresh_token_cookie)
        access_token_cookie_1 = access_token_cookie.value
        refresh_token_cookie_1 = refresh_token_cookie.value
        id_refresh_token_cookie_1 = id_refresh_token_cookie.value

        response = HttpResponse()
        supertokens.create_new_session(
            response, user_id, jwt_payload, session_data)

        access_token_cookie = response.cookies.get("sAccessToken")
        refresh_token_cookie = response.cookies.get("sRefreshToken")
        id_refresh_token_cookie = response.cookies.get(
            "sIdRefreshToken")
        self.assertTrue(response.has_header("ANTI-CSRF"))
        anti_csrf_token_2 = response.get("ANTI-CSRF")

        self.assertIsNotNone(access_token_cookie)
        self.assertIsNotNone(refresh_token_cookie)
        self.assertIsNotNone(id_refresh_token_cookie)
        access_token_cookie_2 = access_token_cookie.value
        refresh_token_cookie_2 = refresh_token_cookie.value
        id_refresh_token_cookie_2 = id_refresh_token_cookie.value

        response = HttpResponse()
        supertokens.create_new_session(
            response, user_id, jwt_payload, session_data)

        access_token_cookie = response.cookies.get("sAccessToken")
        refresh_token_cookie = response.cookies.get("sRefreshToken")
        id_refresh_token_cookie = response.cookies.get(
            "sIdRefreshToken")
        self.assertTrue(response.has_header("ANTI-CSRF"))
        anti_csrf_token_3 = response.get("ANTI-CSRF")

        self.assertIsNotNone(access_token_cookie)
        self.assertIsNotNone(refresh_token_cookie)
        self.assertIsNotNone(id_refresh_token_cookie)
        access_token_cookie_3 = access_token_cookie.value
        refresh_token_cookie_3 = refresh_token_cookie.value
        id_refresh_token_cookie_3 = id_refresh_token_cookie.value

        supertokens.revoke_all_sessions_for_user(user_id)

        request = request = self.factory.get('/')
        request.COOKIES["sAccessToken"] = access_token_cookie_1
        request.COOKIES["sIdRefreshToken"] = id_refresh_token_cookie_1
        request.COOKIES["sRefreshToken"] = refresh_token_cookie_1
        response = HttpResponse()
        try:
            supertokens.refresh_session(request, response)
            self.assertTrue(False)
        except SuperTokensUnauthorizedException:
            self.assertTrue(True)

        request = request = self.factory.get(
            '/', **{'HTTP_' + "ANTI_CSRF": anti_csrf_token_1})
        request.COOKIES["sAccessToken"] = access_token_cookie_1
        request.COOKIES["sIdRefreshToken"] = id_refresh_token_cookie_1
        response = HttpResponse()
        try:
            supertokens.get_session(request, response, True)
            self.assertTrue(False)
        except SuperTokensUnauthorizedException:
            self.assertTrue(True)

        request = request = self.factory.get('/')
        request.COOKIES["sAccessToken"] = access_token_cookie_2
        request.COOKIES["sIdRefreshToken"] = id_refresh_token_cookie_2
        request.COOKIES["sRefreshToken"] = refresh_token_cookie_2
        response = HttpResponse()
        try:
            supertokens.refresh_session(request, response)
            self.assertTrue(False)
        except SuperTokensUnauthorizedException:
            self.assertTrue(True)

        request = request = self.factory.get(
            '/', **{'HTTP_' + "ANTI_CSRF": anti_csrf_token_2})
        request.COOKIES["sAccessToken"] = access_token_cookie_2
        request.COOKIES["sIdRefreshToken"] = id_refresh_token_cookie_2
        response = HttpResponse()
        try:
            supertokens.get_session(request, response, True)
            self.assertTrue(False)
        except SuperTokensUnauthorizedException:
            self.assertTrue(True)

        request = request = self.factory.get('/')
        request.COOKIES["sAccessToken"] = access_token_cookie_3
        request.COOKIES["sIdRefreshToken"] = id_refresh_token_cookie_3
        request.COOKIES["sRefreshToken"] = refresh_token_cookie_3
        response = HttpResponse()
        try:
            supertokens.refresh_session(request, response)
            self.assertTrue(False)
        except SuperTokensUnauthorizedException:
            self.assertTrue(True)

        request = request = self.factory.get(
            '/', **{'HTTP_' + "ANTI_CSRF": anti_csrf_token_3})
        request.COOKIES["sAccessToken"] = access_token_cookie_3
        request.COOKIES["sIdRefreshToken"] = id_refresh_token_cookie_3
        response = HttpResponse()
        try:
            supertokens.get_session(request, response, True)
            self.assertTrue(False)
        except SuperTokensUnauthorizedException:
            self.assertTrue(True)
