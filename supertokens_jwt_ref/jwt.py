from .utils import (
    base64decode,
    base64encode,
    hmac_hex_digest
)
from json import (
    dumps,
    loads
)

_header = base64encode(dumps({
    "alg": "HS256",
    "typ": "JWT"
}))


def encode(plaintext_payload, signingkey):
    payload = base64encode(dumps(plaintext_payload))
    signature = hmac_hex_digest(signingkey, _header + "." + payload)
    return _header + "." + payload + "." + signature


def decode(jwt, signingkey):
    splitted_input = jwt.split(".")

    if len(splitted_input) != 3:
        raise Exception("invalid jwt")

    if splitted_input[0] != _header:
        raise Exception("jwt header mismatch")

    payload = splitted_input[1]
    signature_from_jwt = hmac_hex_digest(signingkey, _header + "." + payload)

    if signature_from_jwt != splitted_input[2]:
        raise Exception("jwt verification failed")

    payload = base64decode(payload)
    return loads(payload)
