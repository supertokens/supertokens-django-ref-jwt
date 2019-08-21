from base64 import b64encode, b64decode
import hmac
from hashlib import pbkdf2_hmac, md5, sha256
import random
from string import ascii_lowercase, digits
from uuid import uuid4
from Crypto.Cipher import AES
from json import dumps, loads
from .exceptions import raise_general_exception
from django.conf import settings
from django.utils import timezone


def base64encode(s):
    return b64encode(s.encode()).decode()


def base64decode(s):
    return b64decode(s.encode()).decode()


def hmac_hex_digest(key, data):
    return hmac.new(key.encode(), data.encode(), sha256).hexdigest()


def get_random_bytes(size):
    return "".join([random.choice(ascii_lowercase + digits) for n in range(size)]).encode()


def generate_new_signing_key():
    return b64encode(pbkdf2_hmac("sha256", get_random_bytes(64), get_random_bytes(64), 32, 100)).decode()


def generate_uuid():
    return str(uuid4())


def custom_hash(s):
    return sha256(s.encode()).hexdigest()


def encrypt(plaintext, masterkey):
    iv = get_random_bytes(16)
    salt = get_random_bytes(64)
    key = md5(b64encode(pbkdf2_hmac(
        "sha256", masterkey.encode(), salt, 32, 100))).hexdigest()
    cipher = AES.new(key.encode(), AES.MODE_GCM)
    encrypted, tag = cipher.encrypt_and_digest(plaintext.encode())
    encrypted = b64encode(encrypted)
    tag = b64encode(tag)
    nonce = b64encode(cipher.nonce)
    ciphertext = b64encode(salt + iv + tag + nonce + encrypted).decode()
    return ciphertext


def decrypt(encrypted_data, masterkey):
    b_data = base64decode(encrypted_data)
    salt = b_data[0:64].encode()
    tag = b64decode(b_data[80:104])
    nonce = b64decode(b_data[104:128])
    text = b64decode(b_data[128:])
    key = md5(b64encode(pbkdf2_hmac(
        "sha256", masterkey.encode(), salt, 32, 100))).hexdigest()
    cipher = AES.new(key.encode(), AES.MODE_GCM, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(text, tag)
    return plaintext.decode()


def sanitize_string(s):
    if s == "":
        return s

    if not isinstance(s, str):
        return None

    return s.strip()


def sanitize_number(n):
    _type = type(n)
    if _type == int or _type == float:
        return n

    return None


def serialize_data(d):
    return "" if d is None else dumps(d)


def unserialize_data(d):
    return None if d == "" else loads(d)


def assert_user_id_has_correct_format(user_id):
    if not isinstance(user_id, str) and not isinstance(user_id, int):
        raise_general_exception('user id must be string or number')


def serialize_user_id(user_id):
    assert_user_id_has_correct_format(user_id)
    if isinstance(user_id, str):
        is_parsing_error = True
        try:
            json_from_user_id = loads(user_id)
            is_parsing_error = False
            if isinstance(json_from_user_id, dict) and len(json_from_user_id) == 1 and 'i' in json_from_user_id:
                raise_general_exception(
                    "passed userId cannot be stringified version of object type {i: string}")
        except Exception as e:
            if is_parsing_error:
                pass
            else:
                raise e
        return user_id
    else:
        return dumps({'i': user_id})


def unserialize_user_id(user_id):
    try:
        id = loads(user_id)
        if isinstance(id, dict) and len(id) == 1 and 'i' in id:
            return id['i']
    except Exception:
        pass
    return user_id


def get_timezone():
    return timezone.utc if settings.USE_TZ else None
