from supertokens_jwt_ref import jwt
from django.test import TestCase


class JwtTest(TestCase):

    def test_encode_and_decode(self):
        data = {"a": "testing"}
        key = "supertokens"
        enocoded_data = jwt.encode(data, key)
        decoded_data = jwt.decode(enocoded_data, key)
        self.assertDictEqual(data, decoded_data)

    def test_encode_and_decode_different_keys(self):
        data = {"a": "testing"}
        key = "supertokens"
        enocoded_data = jwt.encode(data, key)
        try:
            jwt.decode(enocoded_data, "wrong_key")
            self.assertTrue(False)
        except BaseException:
            self.assertTrue(True)
