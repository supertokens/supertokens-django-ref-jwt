from supertokens_session import cookie
from django.http import HttpRequest, HttpResponse
from django.test import TestCase
from datetime import datetime, timedelta

class CookieTest(TestCase):

    def test_set_cookie(self):
        response = HttpResponse()

        key = 'test'
        value = 'value'
        expires = datetime.now() + timedelta(seconds=60)
        path = '/'
        domain = 'localhost'
        secure = False
        httponly = False

        cookie.set_cookie(response, key, value, expires, path, domain, secure, httponly)
        