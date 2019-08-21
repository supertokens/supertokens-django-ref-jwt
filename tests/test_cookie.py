from supertokens_jwt_ref import cookie_and_header
from django.http import HttpResponse
from django.test import TestCase, RequestFactory
from datetime import datetime, timedelta
from supertokens_jwt_ref.utils import get_timezone


class CookieTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_set_cookie(self):
        response = HttpResponse()

        key = 'test'
        value = 'value'
        expires = datetime.now(tz=get_timezone()) + timedelta(seconds=60)
        path = '/'
        domain = 'localhost'
        secure = True
        httponly = True

        cookie_and_header.set_cookie(response, key, value,
                                     expires.timestamp(), path, domain, secure, httponly)
        # will return None if no cookie with this key is found
        cookie_obj = response.cookies.get(key)
        self.assertIsNotNone(cookie_obj)
        # value property is directly available on cookie object
        # for other attributes, they are stored as dict in cookie object
        # available attributes via dict:
        # expires, path, comment, domain, max-age, secure, httponly, version, samesite
        # NOTE: max_age=None, expires=None, domain=None, secure=False, httponly=False
        #       if domain value is not set or is set to None, it's value will be ''
        #       if secure value is not set or is set to False, it's value will be ''
        #       if httponly value is not set or is set to False, it's value will be ''
        #       if both, max_age and expires value are not set or are set to None, it's value will be ''
        self.assertEqual(cookie_obj.value, value)
        self.assertEqual(cookie_obj['path'], path)
        self.assertEqual(cookie_obj['domain'], domain)
        self.assertEqual(cookie_obj['httponly'], secure)
        self.assertEqual(cookie_obj['secure'], httponly)
        self.assertEqual(cookie_obj['expires'], expires.strftime(
            '%a, %d %b %Y %H:%M:%S GMT'))

    def test_get_cookie(self):
        key = 'test'
        value = 'value'

        request = self.factory.get('/')
        request.COOKIES[key] = value

        self.assertEqual(cookie_and_header.get_cookie(request, key), value)

    def test_get_header(self):
        key = 'TEST'
        value = 'value'

        request = self.factory.get('/', **{'HTTP_' + key: value})
        self.assertEqual(cookie_and_header.get_header(request, key), value)

    def test_set_header(self):
        response = HttpResponse()
        key = 'HTTP_TEST'
        value = 'value'

        cookie_and_header.set_header(response, key, value)
        self.assertTrue(response.has_header(key))
        self.assertEqual(response.get(key), value)
