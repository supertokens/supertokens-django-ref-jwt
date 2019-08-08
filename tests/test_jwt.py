from supertokens_session import jwt
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
        error = False
        try:
            decoded_data = jwt.decode(enocoded_data, "wrong_key")
            error = True
        except:
            self.assertTrue(True)

        if error:
            raise Exception('jwt verified with wrong signing key')