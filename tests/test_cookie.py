from supertokens_session import cookie
from django.http import HttpRequest, HttpResponse
from django.test import TestCase, RequestFactory
from datetime import datetime, timedelta

class CookieTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_set_cookie(self):
        response = HttpResponse()

        key = 'test'
        value = 'value'
        expires = datetime.now() + timedelta(seconds=60)
        path = '/'
        domain = 'localhost'
        secure = True
        httponly = True

        cookie.set_cookie(response, key, value, expires, path, domain, secure, httponly)
        cookie_obj = response.cookies.get(key) # will return None if no cookie with this key is found
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
        self.assertEqual(cookie_obj['expires'], expires.strftime('%a, %d %b %Y %H:%M:%S GMT'))

    def test_get_cookie(self):
        key = 'test'
        value = 'value'

        request = self.factory.get('/')
        request.COOKIES[key] = value

        self.assertEqual(cookie.get_cookie(request, key), value)

    def test_get_header(self):
        key = 'TEST'
        value = 'value'

        request = self.factory.get('/', **{'HTTP_' + key: value})
        self.assertEqual(cookie.get_header(request, key), value)

    def test_set_header(self):
        response = HttpResponse()
        key = 'HTTP_TEST'
        value = 'value'

        cookie.set_header(response, key, value)
        self.assertTrue(response.has_header(key))
        self.assertEqual(response.get(key), value)